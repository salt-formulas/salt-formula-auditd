{%- from "auditd/map.jinja" import audisp with context %}

{%- if audisp.get('enabled', False) %}

include:
  - auditd.service

audisp_packages:
  pkg.installed:
    - names: {{ audisp.pkgs }}

  {%- for plugin, plugin_params in audisp.plugins.items() %}
{{ audisp.config_path }}/{{ plugin }}.conf:
  file.managed:
    - source: salt://auditd/files/audisp.plugin.conf
    - template: jinja
    - context:
      params: {{ plugin_params }}
    - user: root
    - group: root
    - mode: 0640
    - require:
      - pkg: audisp_packages
    - watch_in:
      - service: auditd_service
  {%- endfor %}
{%- endif %}
