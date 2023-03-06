# NGINX TEMPLATING ENGINE
---

- all templates written to ./templates/out


### TEMPLATE WORKFLOW
---

### ./templates
- add actual jinja template file here


### ./templates/config 
- add JSON data corresponding to a template with same filename


#### .env (both files should have same name, minus extension)
- add filename created in ./templates
- add filename created in ./templates/config


#### ./conf/clsCfgs.py 
- add new method that returns template name, out_dir, & template context data
  

#### ./main.py
- import newly created methods from ./conf/clsCfgs.py
- use NginxTemplater.create_and_save_template to see if it works