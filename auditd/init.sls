include:
{%- if pillar.auditd.service is defined %}
  - auditd.service
{%- if pillar.auditd.audisp is defined %}
  - auditd.audisp
{%- endif %}
{%- if pillar.auditd.rules is defined %}
  - auditd.rules
{%- endif %}
{% endif %}
