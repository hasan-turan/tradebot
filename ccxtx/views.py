from django.shortcuts import render
import ccxt
from .models import Ccxtx
from .forms import CcxtxForm

from bokeh.client import pull_session
from bokeh.embed import server_session
from bokeh.util import session_id
# Create your views here.
def ccxtx_index(request):

    bokehServerUrl = 'http://localhost:5006/bokeh_server'

    script = server_session(model=None,
                            session_id=session_id.generate_session_id(),
                            url=bokehServerUrl,
                            )
   
   
    form = CcxtxForm(request.POST or None)
    
    context = {
        'form': form,
        'script': script
    }
    return render(request, 'ccxtx/index.html',context)

   
