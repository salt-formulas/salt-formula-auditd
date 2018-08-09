{%- from "auditd/map.jinja" import service with context %}

{%- if service.get('enabled', false) %}
auditd_packages:
  pkg.installed:
    - names: {{ service.pkgs }}

auditd_service:
  service.running:
    - enable: true
    - running: true
    - name: {{ service.name }}
    - require:
      - pkg: auditd_packages
    - retry:
        attempts: 3
        interval: 10

/etc/audit/auditd.conf:
  file.managed:
    - source: salt://auditd/files/auditd.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 0640
    - require:
      - pkg: auditd_packages
    - watch_in:
      - service: auditd_service

{%- endif %}
