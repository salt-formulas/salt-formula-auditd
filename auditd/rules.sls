{%- from "auditd/map.jinja" import rules with context %}

include:
  - auditd.service

/etc/audit/audit.rules:
  file.managed:
    - source: salt://auditd/files/auditd.rules.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 0640
    - require:
      - pkg: auditd_packages
    - watch_in:
      - service: auditd_service

{%- if grains.get('virtual_subtype', None) not in ['Docker', 'LXC'] %}
reload_rules:
  cmd.run:
    - name: /sbin/auditctl -R /etc/audit/audit.rules
    - onchanges:
      - file: /etc/audit/audit.rules
    - require:
      - service: auditd_service
{%- endif %}
