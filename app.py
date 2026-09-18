import streamlit as st
import pandas as pd

st.set_page_config(page_title="Анализ Мутаций ДНК", layout="wide", page_icon="🧬 ")

# --- БОКОВАЯ ПАНЕЛЬ (СПРАВОЧНИК) ---
st.sidebar.title("📚 Справочник")
st.sidebar.info("ДНК ➔ мРНК ➔ Белок")

st.sidebar.markdown("""
### 1. Нуклеотиды ДНК
* **A** — Аденин
* **T** — Тимин
* **G** — Гуанин
* **C** — Цитозин

### 2. Транскрипция
При переходе в мРНК тимин (**T**) заменяется на урацил (**U**).

### 3. Мутации
**Замена:** изменение одного нуклеотида. Может менять аминокислоту в белке.
""")

# --- ОСНОВНАЯ СТРАНИЦА ---
st.title("🧬  Анализатор ДНК, Трансляция и Поиск Мутаций")
st.write("Сервис для трансляции последовательностей и анализа генных мутаций.")

# --- ИНСТРУКЦИЯ / ТУТОРИАЛ ---
st.success("""
👉 **Быстрый старт:** 
1. Введите исходную цепь ДНК слева и мутировавшую справа.
2. Нажмите кнопку **«Запустить биоинформатический анализ»**.
3. Изучите транскрипцию, трансляцию и найденные мутации в таблице ниже!
""")

st.markdown("---")

CODON_TABLE = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 'TGA':'_'
}

def dna_to_rna(dna):
    return dna.replace('T', 'U')

def translate_dna(dna):
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3]
        protein += CODON_TABLE.get(codon, '?')
    return protein

# Ввод данных
col1, col2 = st.columns(2)

with col1:
    dna_input = st.text_area("Исходная последовательность ДНК (Исходный ген):", "ATGCGATCGATCGTTTAG").upper().strip()

with col2:
    mutated_dna = st.text_area("Мутировавшая последовательность ДНК:", "ATGCGACCGATCGTTTAG").upper().strip()

if st.button("🧬  Запустить биоинформатический анализ"):
    rna = dna_to_rna(dna_input)
    protein_orig = translate_dna(dna_input)
    protein_mut = translate_dna(mutated_dna)
    
    st.markdown("---")
    st.subheader("1. Транскрипция и Трансляция")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.write("**мРНК (Исходная):**")
        st.code(rna)
        st.write("**Белковая цепь (Исходная):**")
        st.code(protein_orig)
        
    with res_col2:
        st.write("**мРНК (Мутировавшая):**")
        st.code(dna_to_rna(mutated_dna))
        st.write("**Белковая цепь (Мутировавшая):**")
        st.code(protein_mut)
        
    st.markdown("---")
    st.subheader("2. Сравнение и поиск мутаций")
    
    min_len = min(len(dna_input), len(mutated_dna))
    mutations = []
    
    for idx in range(min_len):
        if dna_input[idx] != mutated_dna[idx]:
            mutations.append({
                "Позиция": idx + 1,
                "Было (Исходный)": dna_input[idx],
                "Стало (Мутация)": mutated_dna[idx]
            })
            
    if mutations:
        st.warning(f"Найдено мутаций: {len(mutations)}")
        st.table(pd.DataFrame(mutations))
    else:
        st.success("Последовательности идентичны! Мутаций не обнаружено.")
