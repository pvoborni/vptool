import os
import subprocess

def run(args):
    child = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = child.communicate()
    rc = child.returncode

    return stdout, stderr, rc


def require_root():
    if os.geteuid() != 0:
        raise RuntimeError("You need to run this script as a root.")


def normalize_hostname(ip):
    last_ip_segment = ip.split('.')[-1]

    return 'vm-%s' % normalize_ip_suffix(last_ip_segment)


def normalize_ip_suffix(last_ip_segment):

    if len(last_ip_segment) == 1:
        return '00%s' % last_ip_segment
    elif len(last_ip_segment) == 2:
        return '0%s' % last_ip_segment
    else:
        return '%s' % last_ip_segment

def get_latest_template(api, name):
    templates = api.templates.list(query="name=%s" % name)

    if len(templates) == 0:
	# No template found, return None
	return None
    elif len(templates) == 1:
	# Only one template exists with the name, return it
	return templates[0]
    else:
	# Pick the latest template
	versioned_templates = [temp for temp in templates if temp.get_version()]
	return max(versioned_templates,
		   key=lambda t: t.get_version().get_version_number())
