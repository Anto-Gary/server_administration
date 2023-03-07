# NGINX TEMPLATING ENGINE
---

- all templates written to ./templates/out by default
  - subdir name 'out' can be changed in TemplateEngine.py


### TEMPLATE WORKFLOW
---

#### ./templates
- add actual jinja template file here


#### ./templates/context 
- add JSON data corresponding to a template, with same filename as template it's to be used with
- subdir name 'context' can be changed in TemplateEngine.py, class specifically looks for ./templates/context


#### .env
- add filename created in ./templates
  - should have same name, minus extension, as context file in ./templates/context


#### ./conf/clsCfgs.py 
- add new method that returns template name
  

#### ./main.py
- import newly created methods from ./conf/clsCfgs.py
- create a method like NginxTemplater.create_reverse_proxy_template