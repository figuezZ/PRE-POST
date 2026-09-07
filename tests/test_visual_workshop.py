"""Verificaciones independientes del taller (sin navegador ni red).

Referencia: integrales de área, primer/segundo momento y equilibrio elástico.
El cálculo de control integra respecto de la base, no copia el algoritmo de
ejes paralelos que ejecuta JavaScript.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest


HTML = Path(__file__).resolve().parents[1] / 'standalone/PRE_POST_Standalone.html'
pytestmark = pytest.mark.skipif(shutil.which('node') is None, reason='Node requerido')


def run_js(code):
    source = re.search(r'<script id="prepost-core">(.*?)</script>', HTML.read_text(), re.S)[1]
    process = subprocess.run(['node', '-e', source + '\n' + code], capture_output=True, text=True, check=True)
    return json.loads(process.stdout)


def part(b, h, y=0, sign=1):
    return dict(b=b, h=h, y=y, sign=sign, name='Control')


SHAPES = [
    [part(.4, .8)],
    [part(.12, .64), part(.4, .16, .64)],
    [part(.32, .144), part(.1, .48, .144), part(.4, .176, .624)],
    [part(.4, .8), part(.2, .48, .16, -1)],
    [part(.5, 1), part(.1, .2, .8, -1)],  # rebaje superior
]


def reference(parts):
    area = sum(p['sign'] * p['b'] * p['h'] for p in parts)
    first = sum(p['sign'] * p['b'] * ((p['y']+p['h'])**2-p['y']**2)/2 for p in parts)
    second = sum(p['sign'] * p['b'] * ((p['y']+p['h'])**3-p['y']**3)/3 for p in parts)
    cy = first/area
    inertia = second-area*cy**2
    height = max(p['y']+p['h'] for p in parts if p['sign'] == 1)
    return area, cy, inertia, height


@pytest.mark.parametrize('parts', SHAPES)
def test_component_properties_against_integrals(parts):
    s = run_js(f'console.log(JSON.stringify(PrePostCore.componentProperties({json.dumps(parts)},25000)));')
    area, cy, inertia, height = reference(parts)
    assert s['area_m2'] == pytest.approx(area)
    assert s['centroid_from_bottom_m'] == pytest.approx(cy)
    assert s['inertia_m4'] == pytest.approx(inertia)
    assert s['section_modulus_top_m3'] == pytest.approx(inertia/(height-cy))
    assert s['section_modulus_bottom_m3'] == pytest.approx(inertia/cy)
    assert s['self_weight_n_m'] == pytest.approx(area*25000)
    assert sum(r['area']*r['d'] for r in s['rows']) == pytest.approx(0, abs=1e-12)


INVALID = [
    [],
    [part(-.4,.8)],
    [part(.4,.8,sign=0)],
    [part(.4,.8,.1)],
    [part(.4,.5), part(.3,.4,.4)],
    [part(.4,.5), part(.3,.4,.6)],
    [part(.4,.8), part(.5,.4,.1,-1)],
    [part(.4,.8), part(.1,.4,.6,-1)],
    [part(.4,.8), part(.1,.4,.1,-1),part(.1,.4,.2,-1)],
    [part(.4,.8), part(.4,.8,0,-1)],
    [part(.4,.8), part(.2,.8,0,-1)],
]


@pytest.mark.parametrize('parts', INVALID)
def test_invalid_geometries_are_rejected(parts):
    outcome = run_js(f'''try {{ PrePostCore.componentProperties({json.dumps(parts)},25000);
console.log(false); }} catch(error) {{console.log(true);}}''')
    assert outcome


@pytest.mark.parametrize('parts', SHAPES)
def test_stress_equilibrium_and_memory_for_both_stages(parts):
    area, cy, inertia, height = reference(parts)
    payload = dict(span_m=10, width_m=.4, height_m=.8, fci_pa=35e6, fc_pa=45e6,
                   unit_weight_n_m3=25000, dead_load_n_m=1200, live_load_n_m=5000,
                   initial_force_n=100000, steel_area_m2=.0007,
                   eccentricity_m=height*.1-cy, loss_ratio=.15, components=parts)
    result = run_js(f'''
const r=PrePostCore.analyze({json.dumps(payload)});
console.log(JSON.stringify(['transfer','service'].flatMap(stage=>[0,2.5,5,10].map(x=>({{
  stage,x,at:PrePostCore.stageAt(r,stage,x),memo:PrePostCore.memory(r,stage,x),
  fiber:PrePostCore.fiberAt(r,stage,x,0)
}})))));
''')
    for item in result:
        force = 100000 if item['stage'] == 'transfer' else 85000
        w = area*25000 + (0 if item['stage'] == 'transfer' else 6200)
        x = item['x']
        moment = w*x*(10-x)/2
        resultant = force*payload['eccentricity_m']+moment
        stress = item['at']['stress']
        assert stress['top_pa'] == pytest.approx(-force/area-resultant*(height-cy)/inertia)
        assert stress['bottom_pa'] == pytest.approx(-force/area+resultant*cy/inertia)
        assert item['fiber']['stress'] == pytest.approx(-force/area)
        assert item['at']['shear'] == pytest.approx(w*(5-x))
        assert item['memo'][-2]['value'] == pytest.approx(stress['top_pa'])
        assert item['memo'][-1]['value'] == pytest.approx(stress['bottom_pa'])
        assert all(s['formula'] and s['substitution'] and s['reference'] for s in item['memo'])
        assert len(item['memo']) == 19
        # Integrar σ dA = −P y σ y dA = −Mr para toda la sección.
        assert stress['axial_component_pa']*area == pytest.approx(-force)
        assert item['at']['slope']*inertia == pytest.approx(-resultant)
        if item['at']['zero'] is not None:
            assert stress['axial_component_pa'] + item['at']['slope']*item['at']['zero'] == pytest.approx(0,abs=1e-8)


def test_tendon_in_void_and_nonfinite_e_are_rejected():
    output = run_js('''
const base={span_m:10,width_m:.4,height_m:.8,fci_pa:35e6,fc_pa:45e6,
unit_weight_n_m3:25000,dead_load_n_m:0,live_load_n_m:0,initial_force_n:1e5,
steel_area_m2:.001,loss_ratio:0,eccentricity_m:0,
components:[{b:.4,h:.8,y:0,sign:1},{b:.2,h:.4,y:.2,sign:-1}]};
console.log(JSON.stringify([0,NaN,Infinity].map(e=>{try {PrePostCore.analyze({...base,eccentricity_m:e});return false;}catch(err){return true;}})));
''')
    assert all(output)


def test_si_uscs_roundtrip_all_workshop_dimensions():
    result = run_js('''console.log(JSON.stringify(Object.keys(PrePostCore.units.SI).map(q=>
PrePostCore.toSI(PrePostCore.fromSI(.123456789,q,'USCS'),q,'USCS'))));''')
    assert result == pytest.approx([.123456789]*11)


def test_uniform_compression_has_no_zero_line_and_profile_uses_real_centroid():
    result = run_js('''
const r=PrePostCore.analyze({span_m:10,width_m:.4,height_m:.8,fci_pa:35e6,fc_pa:45e6,unit_weight_n_m3:25000,
dead_load_n_m:0,live_load_n_m:0,initial_force_n:100000,steel_area_m2:.001,loss_ratio:0,eccentricity_m:0});
console.log(JSON.stringify({at:PrePostCore.stageAt(r,'transfer',0),profile:PrePostCore.stressProfile(1,2,4,3,.6)}));
''')
    assert result['at']['zero'] is None
    assert result['at']['stress']['top_pa'] == result['at']['stress']['bottom_pa']
    assert result['profile'][0]['x'] == -.6
    assert result['profile'][-1]['x'] == .4


def test_streamlit_can_open_workshop():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(HTML.parents[1]/'src/app/app.py')).run(timeout=20)
    app.selectbox[0].set_value('Taller visual: secciones, memoria y tensiones').run(timeout=20)
    assert not app.exception
    assert any(b.label == 'Descargar taller HTML local' for b in app.download_button)
    assert len(app.get('iframe')) == 1


def test_diagram_extremes_and_invalid_sampling():
    result=run_js('''
const d=PrePostCore.beamDiagram(8000,10);
const invalid=[()=>PrePostCore.beamDiagram(8000,10,1),()=>PrePostCore.beamDiagram(-1,10),
()=>PrePostCore.stressProfile(0,1,2),()=>PrePostCore.stressProfile(1,Infinity,2)];
console.log(JSON.stringify({start:d[0],mid:d[50],end:d[100],invalid:invalid.map(f=>{try{f();return false;}catch(e){return true;}})}));
''')
    assert result['start']['shear'] == 40000
    assert result['mid']['moment'] == 100000
    assert result['end']['moment'] == 0
    assert all(result['invalid'])


def test_explorer_rejects_outside_position_and_fiber():
    result=run_js('''
const r=PrePostCore.analyze({span_m:10,width_m:.4,height_m:.8,fci_pa:35e6,fc_pa:45e6,unit_weight_n_m3:25000,
dead_load_n_m:0,live_load_n_m:0,initial_force_n:100000,steel_area_m2:.001,loss_ratio:0,eccentricity_m:0});
const f=[()=>PrePostCore.stageAt(r,'transfer',11),()=>PrePostCore.stageAt(r,'otra',1),()=>PrePostCore.fiberAt(r,'transfer',1,1)];
console.log(JSON.stringify(f.map(g=>{try{g();return false;}catch(e){return true;}})));
''')
    assert all(result)


def test_static_controls_exist_for_app_bindings():
    html=HTML.read_text()
    markup=html.split('<script id="prepost-core">')[0]
    ids=re.findall(r'\bid="([^"]+)"',markup)
    assert len(ids) == len(set(ids))
    app=re.search(r'<script id="prepost-app">(.*?)</script>',html,re.S)[1]
    references=re.findall(r'''\$\(['"]#([\w-]+)['"]\)''',app)
    assert set(references) <= set(ids)
    assert 'beforeprint' in app and 'afterprint' in app
