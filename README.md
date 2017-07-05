# organization_dashboard_api

## Organization Dashboard API version 1

The APIs in this repository, are for Open edX platform.

### Installation

* Clone the repository:

  https://github.com/DhruvThakker/organization_dashboard_api.git

* Copy the API folder (organization_dashboard_api) to the folder, /edx/app/edxapp/edx-platform/lms/djangoapps/

* Add the name of the app (organization_dashboard_api) in the key ‘INSTALLED_APPS’ in python file /edx/app/edxapp/edx-platform/lms/envs/common.py

```python
INSTALLED_APPS = (

...


‘organization_dashboard_api’ ,


)
```

* Add the urls of the app (organization_dashboard_api) to ‘url_patterns’ in python file /edx/app/edxapp/edx-platform/lms/urls.py

```python
urlpatterns = (

...

url(r’^api/courses’, include(‘organization_dashboard_api.urls’)),

)
```

* Restart LMS and CMS servers by the command:
```bash
sudo /edx/bin/supervisorctl restart edxapp:
```


### [Documentation for APIs](https://github.com/DhruvThakker/organization_dashboard_api/wiki)
