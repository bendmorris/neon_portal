from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from sp_list.models import SpListDocument, ProcessingJob
from sp_list.forms import SpListDocumentForm

import csv
import os
import time
from dodobase.tools.get_site_list import get_site_list
from dodobase.tools.get_spp_list import get_spp_list
from dodobase.tools.config import groups


@login_required
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = SpListDocumentForm(request.POST, request.FILES)
        data = form.data
        if form.is_valid():
            newdoc = SpListDocument(docfile = request.FILES['docfile'], tax_group=data['tax_group'], comments=data['comments'], uploaded_by=request.user)
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('sp_list.views.upload'))
    else:
        form = SpListDocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = SpListDocument.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'upload.html',
        {'documents': documents, 'form': form, 
         'uploader': u'sp_list.add_splistdocument' in request.user.get_all_permissions(),
         'deleter': u'sp_list.delete_splistdocument' in request.user.get_all_permissions()},
        context_instance=RequestContext(request)
    )
    
    
@login_required
def enter(request):
    if request.method == 'POST':
        params = ('site', 'genus', 'sp', 'subsp', 'common_name', 'source')
        all_values = [request.POST.getlist(param) for param in params]
        rows = [params] + zip(*all_values)
        
        taxon = request.POST.get('taxon')
        comments = request.POST.get('comments')
        filename = 'documents/%s.%s.%s.csv' % (request.user.username, taxon, time.strftime('%Y-%h-%d.%H%M%S'))
        output_file = open(filename, 'w')
        output_file.write('\n'.join([','.join(['"%s"' % cell for cell in row]) for row in rows]))
        output_file.close()
        
        newdoc = SpListDocument(docfile=filename, tax_group = taxon, comments=comments, uploaded_by=request.user)
        newdoc.save()

    documents = SpListDocument.objects.all()
        
    return render_to_response(
        'enter.html',
        {'documents': documents,
         'has_permission': u'sp_list.add_splistdocument' in request.user.get_all_permissions(),
         'groups': groups,
         'sites': get_site_list(),
         },
        context_instance=RequestContext(request)
    )
    
    
@login_required
def jobs(request):
    if request.method == 'POST':
        selected_documents = ','.join(request.POST.getlist('document-selector'))
        
        print repr(selected_documents)

        if selected_documents:
            newjob = ProcessingJob(user=request.user, documents=selected_documents)
            newjob.save()
            
        return HttpResponseRedirect(reverse('sp_list.views.jobs'))

    documents = SpListDocument.objects.all()
    jobs = ProcessingJob.objects.all()
    
    return render_to_response(
        'jobs.html',
        {
         'current_jobs': jobs,
         'documents': documents,
         'has_permission': u'sp_list.add_processingjob' in request.user.get_all_permissions(),
         'select_documents': True,
         },
        context_instance=RequestContext(request)
    )
    

@login_required    
def delete(request, id):
    try:
        id = int(id)
        obj = SpListDocument.objects.get(pk=id)
        if str(obj.uploaded_by) == str(request.user.username) or u'sp_list.delete_splistdocument' in request.user.get_all_permissions():
            file_name = obj.docfile
            os.remove(file_name.path)
            obj.delete()
    except Exception as e: print e
    return HttpResponseRedirect(reverse('sp_list.views.upload'))
    

@login_required
def kill(request, id):
    try:
        id = int(id)
        obj = ProcessingJob.objects.get(pk=id)
        if u'sp_list.delete_processingjob' in request.user.get_all_permissions():
            obj.delete()
    except Exception as e: print e
    return HttpResponseRedirect(reverse('sp_list.views.jobs'))
    

@login_required    
def process(request):
    import process_job as p
    p.process_next_job()
    return HttpResponseRedirect(reverse('sp_list.views.jobs'))
    
    
def list(request):
    if request.method == 'POST':
        taxon = request.POST.get('taxon')
        site = request.POST.get('site')
        
        submit_type = request.POST.get('submit')
        if submit_type == 'Download CSV':
            return download_csv(request, taxon, site)

        species_list = get_spp_list(taxon, site)

    else:
        species_list = []
        site = None
        taxon = None
        
    sites = get_site_list()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'sites': sites, 'groups':groups, 'species_list': species_list, 'selected_site': site, 'selected_group': taxon},
        context_instance=RequestContext(request)
    )
    
    
def download_csv(request, taxon, site):
    species_list = get_spp_list(taxon, site)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.%s.csv' % (site, taxon)

    writer = csv.writer(response)
    writer.writerow(['site_id','spp_id','sci_name','com_name'])
    for species in species_list:
        writer.writerow((site,) + species)
        
    return response
