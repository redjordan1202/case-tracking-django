from decouple import Config, RepositoryEnv

part_msg ="""Hello,
This is to let you know that the following parts have shipped.
%s
Your %s tracking number is: %s
Please allow up to 48 hours for the tracking to fully update.
Best Regards,
Jordan
Customer Support
Skytech Gaming"""
repair_msg = """Hello,
This is to let you know that your repaired Computer has shipped.
Your %s tracking number is: %s
Our Repair team performed the following Repairs:
'%s'
Please allow up to 48 hours for the tracking to fully update.
Best Regards,
Jordan
Customer Support
Skytech Gaming"""
replace_msg = """Hello,
This is to let you know that your replacement Computer has shipped.
Your %s tracking number is: %s
Please allow up to 48 hours for the tracking to fully update.
Best Regards,
Jordan
Customer Support
Skytech Gaming"""
part_with_label_msg = """Hello,
This is to let you know that the following parts have shipped.
%s
Your %s tracking number is: %s
Please allow up to 48 hours for the tracking to fully update.
===========
A return label has been included with your replacement item. Please use the packaging that your replacement item arrived in to send us back the original defective part using the provided return label at your earliest convenience.
If you need any assistance with sending back the item, please let us know and we can try to accommodate any mitigating circumstances. Refusal to return the original part using the included return label may result in your warranty being voided.
Best Regards,
Jordan
Customer Support
Skytech Gaming"""

envfile = '/var/www/python/case_tracking/cases/.env'
env_config = Config(RepositoryEnv(envfile))
sf_user = env_config.get('sf_user')
sf_passwd = env_config.get('sf_passwd')
sf_token= env_config.get('sf_token')
