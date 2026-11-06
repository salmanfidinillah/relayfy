import os
bind='0.0.0.0:'+os.getenv('PORT','8000')
workers=1
threads=4
timeout=90
graceful_timeout=90
accesslog=None
errorlog='-'
# Never trust arbitrary forwarded client IPs for rate limits.
forwarded_allow_ips=os.getenv('TRUSTED_PROXY_IPS','127.0.0.1')
