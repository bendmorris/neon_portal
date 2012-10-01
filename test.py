import dodobase.tools.config as config
import dodobase.tools.pg_interface as p

p.get_connection(*config.connection_args)
p.create_databases()
p.push_data()
