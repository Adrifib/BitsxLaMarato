from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from supabase import create_client, Client
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
load_dotenv()

# Variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['DEBUG'] = True
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, email):
        self.id = email


@login_manager.user_loader
def load_user(email):
    return User(email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.user:
                user = User(email)
                login_user(user)
                return redirect(url_for('profile'))
        except Exception as e:
            print(f"Error logging in: {e}")
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user:
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('inici', user_email=email))
        except Exception as e:
            print(f"Error registering: {e}")
        flash('Registration Unsuccessful. Please check your details', 'danger')
    return render_template('register.html')

@app.route('/QR')
def QR():
	user_email = request.args.get('user_email')
    base_url = request.host_url  # Obtén la URL base del servidor
    qr_url = base_url + 'inici?user=' + str(user_email) # Concatenamos la URL de la página de inicio
    return render_template('QR.html', qr_url=qr_url)

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insertardatos')
def insertardatos():
    return render_template('insertardatos.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




do_PCR = False
PCR = False
immunosuprimit = False
tmespecific = False
fumador = False
hipertensio_pulmonar = False
sospites_epital = False
hipoTA = False

tinza = False
cmv = False
pnj = False
pneumonia = False
TEC = False

TRACTAMENTS = {
    'oxigenoterapia': 'OXIGENOTERAPIA Ajustar FiO2 según requerimientos (SatO2 > 92%)',
    'oseltamivir': 'Oseltamivir 75mg/12h v.o.',
    'cefalosporina': 'Cefalosporina 3ªG',
    'levofloxacino': 'Levofloxacino 500 mg/24h v.o.',
    'inhibidor_bomba_protons': 'Omeprazol 20 mg/12-24h e.v.',
    'piperacilina': 'Piperacilina/Tazobactam 4g/0,5g/8h e.v. (ó cefalosporina 3ª generació)',
    'ganciclovir': 'Ganciclovir 5mg/Kg pes/12h e.v.',
    'sulfametoxazol': 'Sulfametoxazol/Trimetoprim 800/160mg/12h e.v.',
    'ac_folic': 'Ac.Folic',
    'oxigenoterapia': 'OXIGENOTERAPIA ajustant FIO2 segons requeriments (SatO2 > 92%)',
    'acetilcisteina': 'N-ACETILCISTEÏNA 600 mg/8h v.o. (potent antioxidant pulmonar)',
    'nebulitacions': 'Nebulitzacions amb 1,5-2cc atrovent + 2cc SF +/- 0,5cc salbutamol',
    'morfina': 'MORFINA 2,5-5mg s.c. puntual si dispnea intensa',
    'hbpm_bemi': 'HBPM: Bemiparina 2500-3500 UI/0,2 mL (segons Kg pes) s.c./dia',
    'hbpm_tinza': ' HBPM (Tinzaparina 20000UI 0,5-0,9 mL (segons Kg pes)) s.c./dia',
    'metilprednis': 'METILPREDNISOLONA (en casos específics): ½-1 mg/Kg pes/d e.v   +  CALCI +Vit D 500mg/400 UI: 2comp/d v.o.',
    'losartan': 'LOSARTAN 50mg/24h v.o. (antiapoptòtic epitelial)',
    'ttmespecific': 'Ttm específic',
}


@app.route('/inici')
def inici():
    return render_template('inici.html')


@app.route('/radiografia-torax', methods=['GET', 'POST'])
def radiografia_torax():
    if request.method == 'POST':
        tiene_infiltrados = request.form.get('tiene_infiltrados') == 'true'
        if tiene_infiltrados:
            return redirect(url_for('sospites_grip_covid'))
        return redirect(url_for('final_felic'))
    return render_template('radiografia-torax.html')

@app.route('/final-felic')
def final_felic():
    return render_template('final-felic.html')

@app.route('/sospites-grip-covid', methods=['GET', 'POST'])
def sospites_grip_covid():
    global do_PCR
    do_PCR = False
    if request.method == 'POST':
        sospites_grip = request.form.get('sospites_grip') == 'true'
        sospites_covid = request.form.get('sospites_covid') == 'true'
        do_PCR = sospites_grip or sospites_covid
        if do_PCR:
            return redirect(url_for('micro_anti_hemo_pcr'))
        return redirect(url_for('micro_anti_hemo'))
    return render_template('sospites-grip-covid.html')

@app.route('/micro-anti-hemo')
def micro_anti_hemo():
    return render_template('micro-anti-hemo.html')

@app.route('/micro-anti-hemo-pcr')
def micro_anti_hemo_pcr():
    return render_template('micro-anti-hemo-pcr.html')

@app.route('/dx-pn', methods=['GET', 'POST'])
def dx_pn():
    global PCR, tmespecific, pneumonia
    PCR, tmespecific, pneumonia = False, False, False
    if request.method == 'POST':
        dx_concret = request.form.get('diagnostic_concretat') == 'true'
        pneumonia = request.form.get('pneumonia') == 'true'
        PCR = request.form.get('pcr_positiva') == 'true'
        if dx_concret:
            if pneumonia:
                if immunosuprimit:
                    return redirect(url_for('sospites_cmv_pnj'))
                return redirect(url_for('tractament'))
            tmespecific = True
            return redirect(url_for('tractament'))
        return redirect(url_for('sospites_tep'))
    if do_PCR:
        return render_template('dx-pn_goc.html')
    return render_template('dx-pn.html')

@app.route('/dx-pn_goc', methods=['GET', 'POST'])
def dx_pn_goc():
    global PCR, tmespecific
    PCR, tmespecific = False, False
    if request.method == 'POST':
        dx_concret = request.form.get('diagnostic_concretat') == 'true'
        pneumonia = request.form.get('pneumonia') == 'true'
        PCR = request.form.get('pcr_positiva') == 'true'
        if dx_concret:
            if pneumonia:
                if immunosuprimit:
                    return redirect(url_for('sospites_cmv_pnj'))
                return redirect(url_for('tractament'))
            tmespecific = True
            return redirect(url_for('tractament'))
        return redirect(url_for('sospites_tep'))
    return render_template('dx-pn_goc.html')

@app.route('/sospites-cmv-pnj', methods=['GET', 'POST'])
def sospites_cmv_pnj():
    global cmv, pnj
    cmv, pnj = False, False
    if request.method == 'POST':
        sospites_cmv = request.form.get('sospites_cmv') == 'true'
        sospites_pnj = request.form.get('sospites_pnj') == 'true'
        if sospites_cmv:
            cmv = True
        if sospites_pnj:
            pnj = True
        return redirect(url_for('tractament'))
    return render_template('sospites-cmv-pnj.html')

@app.route('/sospites-tep', methods=['GET', 'POST'])
def sospites_tep():
    global val_parenq
    val_parenq = False
    if request.method == 'POST':
        sospites_TEP = request.form.get('sospites_tep') == 'true'
        if sospites_TEP:
            return redirect(url_for('angio_ddimer'))
        return redirect(url_for('val_parenq'))
    return render_template('sospites-tep.html')

@app.route('/angio-ddimer')
def angio_ddimer():
    return render_template('angio-ddimer.html')    

@app.route('/tep', methods=['GET', 'POST'])
def tep():
    global tinza, val_parenq, TEC
    tinza, val_parenq = False, False
    if request.method == 'POST':
        TEC = request.form.get('tep') == 'true'
        if TEC:
            tec = True
            return redirect(url_for('tractament'))
        return redirect(url_for('val_parenq'))
    return render_template('tep.html')

@app.route('/val-parenq')
def val_parenq():
    global tmespecific
    tmespecific = True
    return render_template('val-parenq.html')

@app.route('/tractament')
def tractament():
    tractaments_client = []
    if pneumonia:
        if not immunosuprimit:
            tractaments_client.extend(['oseltamivir', 'cefalosporina', 'levofloxacino'])
        else:
            tractaments_client.extend(['piperacilina', 'levofloxacino'])
            if cmv:
                tractaments_client.extend(['ganciclovir'])
            if pnj:
                tractaments_client.extend(['sulfametoxazol','ac_folic'])
    if not TEC:
        tractaments_client.extend(['oxigenoterapia','inhibidor_bomba_protons','acetilcisteina','morfina','hbpm_bemi','metilprednis'])
        if fumador and not hipertensio_pulmonar:
            tractaments_client.append(['nebulitacions'])
        if sospites_epital and not hipoTA:
            tractaments_client.append(['losartan'])
    else:
        tractaments_client.extend(['hbpm_tinza'])
    return render_template('tractament.html', tractaments_client=tractaments_client, TRACTAMENTS=TRACTAMENTS)


@app.route('/rediografia-torax')
@login_required
def rediografia_torax():
    return render_template('rediografia-torax.html')

if __name__ == "__main__":
    app.run(port=5000)
