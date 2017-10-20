from django import forms
from django.forms import Form
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from smarttrashApp.tsbackendconnector import TSBackendConnector
from smarttrashApp.tsconfigurator import TSConfigurator
from smarttrashApp.tskeycloakconnector import TSKeyCloakConnector

REVOKE_URI = ""

configurator = TSConfigurator('config.ini')
configurator.readConfiguration()


def refresh_token():
    return configurator.getKAppToken()


keycloak_connector = TSKeyCloakConnector(client_id=configurator.getKAppKeycloak_Client_ID(),
                                         client_secret=configurator.getKAppKeycloak_Client_SECRET(),
                                         token_uri=configurator.getKAppToken_URI(),
                                         revoke_uri=REVOKE_URI, refresh_token=refresh_token)

connector = TSBackendConnector(baseurl=configurator.getKAppBackend_Base(), get_token=keycloak_connector.access_token,
                               ocp_apim_subscription_key=configurator.getKAppBackend_Subscription(),
                               api_url=configurator.getKAppBackend_API())


def keycloak_access_token():
    ktoken = None
    try:
        ktoken = keycloak_connector.access_token()
    except:
        print("Could not get Token")
    return ktoken


def token(request):
    return render(request, 'smarttrash/token.html', {'token': keycloak_access_token()})


def test(request):
    configurator = TSConfigurator('configv2.ini')
    configurator.readConfiguration()
    configurator.writeConfiguration()
    return HttpResponse("return this string")


def setup_acc(request):
    if request.method == 'POST':
        form = Form(request.POST)
        configurator.setKAppToken(form.data["token"])
        return HttpResponseRedirect('./setup_acc')
    else:
        error_message = request.GET.get('error', default=False)
        if configurator.getKAppToken():
            return render(request, 'smarttrash/setup_acc.html',
                          {'refresh_token': configurator.getKAppToken(),
                           'access_token': keycloak_access_token(),
                           'logged_in': True,
                           'error_message': error_message,
                           'client_id': configurator.getKAppKeycloak_Client_ID(),
                           'keycloak_url': configurator.getKAppKeycloak_URI()
                           })
        else:
            return render(request, 'smarttrash/setup_acc.html',
                          {'logged_in': False,
                           'client_id': configurator.getKAppKeycloak_Client_ID(),
                           'keycloak_url': configurator.getKAppKeycloak_URI()})


def setup_wifi(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            configurator.setWifiSSID(form.data["ssid"])
            configurator.setWifiPassword(form.data["password"])
            # redirect to a new URL:
            return HttpResponseRedirect('./')

    # if a GET (or any other method) we'll create a blank form
    else:
        edit = request.GET.get('edit') in ("true", "True")
        ssid = configurator.getWifiSSID()
        password = configurator.getWifiPassword()
        edit = edit or ssid == "" or password == ""
        pw = '' if password == '' or edit else '123456789'
        form = NameForm(initial={'ssid': ssid, 'password': pw})
        form.fields['ssid'].widget.attrs['readonly'] = not edit
        form.fields['password'].widget.attrs['readonly'] = not edit
    return render(request, 'smarttrash/setup_wifi.html', {'form': form, 'edit': edit})


def setup_list(request):
    if request.method == 'POST':
        form = Form(request.POST)
        configurator.setKAppList(form.data["shopping_list"])
        return HttpResponseRedirect('./setup_list')
    else:
        try:
            lists = connector.get_lists()
            print(lists)
            return render(request, 'smarttrash/setup_list.html',
                          {'available_lists': lists, 'selected_list': configurator.getKAppList(), 'error': False})
        except:
            print("Could not get Lists")
            return render(request, 'smarttrash/setup_list.html',
                          {'available_lists': None, 'selected_list': None, 'error': True})


def setup_configuration(request):
    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            configurator.setMotionSensorDistance(form.cleaned_data["motion_sensor_distance"])
            configurator.setSpeakerMode(form.cleaned_data["speaker_mode"])
            configurator.setUploadMode(form.cleaned_data["upload_mode"])

        return HttpResponseRedirect('./setup_configuration')
    else:
        form = ConfigurationForm(initial={
            'motion_sensor_distance': configurator.getMotionSensorDistance(),
            'speaker_mode': configurator.isSpeakerModeOn(),
            'upload_mode': configurator.getUploadMode()
        })
        return render(request, 'smarttrash/setup_configuration.html', {'form': form})


def create_list(request):
    if request.method == 'POST':
        form = Form(request.POST)
        response_list = connector.create_list([{"color": form.data.get("color"), "title": form.data.get("title")}])
        configurator.setKAppList(response_list[0].get("_id"))
        return HttpResponseRedirect('./setup_list')
    else:
        return HttpResponseRedirect('./setup_list')


def add_item(request):
    if request.method == 'POST':
        form = Form(request.POST)
        print(form.data.get("title"))
        connector.add_list_elem(configurator.getKAppList(), form.data.get("title"), form.data.get("subtitle"))
        return HttpResponseRedirect('./add_item')
    else:
        return render(request, 'smarttrash/add_item.html')


class NameForm(forms.Form):
    ssid = forms.CharField(label='SSID', max_length=100)
    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput(render_value=True))


class ConfigurationForm(forms.Form):
    motion_sensor_distance = forms.DecimalField(required=False)
    speaker_mode = forms.BooleanField(required=False)
    upload_mode = forms.ChoiceField(choices=((1, 'directly'), (2, 'localfirst')), required=False)
