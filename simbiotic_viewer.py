from ursina import *
import pandas as pd
import numpy as np

app = Ursina()
window.title = "SPHY PHASE INTERFACE - BLACK HOLE DE-COHERENCE"
window.color = color.black

# Carregar Dados Auditáveis
# O rastro de fase SHA-256 está embutido em cada frame
df = pd.read_parquet("sphy_blackhole_data.parquet")
frames = [df[df['frame'] == f] for f in df['frame'].unique()]
grid_size = int(np.sqrt(len(frames[0])))

# Malha do Tecido do Espaço-Tempo (Sovereign Intellectualism Protocol)
mesh_entity = Entity(model=Mesh(
    vertices=[Vec3(0,0,0) for _ in range(grid_size**2)],
    triangles=[(i, i+1, i+grid_size) for x in range(grid_size-1) for y in range(grid_size-1) for i in [x*grid_size+y] for _ in [0]] +
              [(i+1, i+grid_size+1, i+grid_size) for x in range(grid_size-1) for y in range(grid_size-1) for i in [x*grid_size+y] for _ in [0]],
    mode='triangle'
), double_sided=True)

# HUD de Auditoria - Onde o físico verá a "respiração" do vácuo
label = Text(text="STATUS: EXECUTANDO CÓDIGO-FONTE", position=(-0.85, 0.45), color=color.cyan)
hash_display = Text(text="HASH: ", position=(-0.85, 0.40), scale=0.7)

idx = 0

def update():
    global idx
    current_frame = frames[idx]
    
    zs = current_frame['z'].values
    xs = current_frame['x'].values
    ys = current_frame['y'].values
    
    # Atualiza a geometria em tempo real para mostrar a simetria rotacional
    mesh_entity.model.vertices = [Vec3(xs[i], zs[i], ys[i]) for i in range(len(zs))]
    
    # Coloração por Tensão de Fase (Maxwell-Deywe Formalism)
    # Roxo (Matriz 280) para Matéria, Amarelo (Matriz 60) para Calor/Radiação
    cor_materia = color.color(280, 1, 1) 
    cor_radiacao = color.color(60, 1, 1)
    
    mesh_entity.model.colors = [lerp(cor_materia, cor_radiacao, clamp(abs(z)*2, 0, 1)) for z in zs]
    
    # Exibir a assinatura criptográfica pulsante
    hash_display.text = f"SHA-256: {current_frame['sha256_signature'].iloc[0][:32]}..."
    
    mesh_entity.model.generate()
    idx = (idx + 1) % len(frames)

EditorCamera() # Permite a auditoria visual de simetria por qualquer ângulo
app.run()
