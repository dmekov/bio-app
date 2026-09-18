import streamlit as st
import pandas as pd

st.set_page_config(page_title="Анализ Мутаций ДНК & Обучение", layout="wide", page_icon="🧬 ")

# --- БОКОВАЯ ПАНЕЛЬ: БАЗА ЗНАНИЙ (СПРАВОЧНИК) ---
st.sidebar.title("📚 Справочник биоинформатика")
st.sidebar.info(
    "**Центральная догма молекулярной биологии:**\n\n"
    "**ДНК** ➔ *(Транскрипция)* ➔ **РНК** ➔ *(Трансляция)* ➔ **Белок**"
)

with st.sidebar.expander("📖  1. Базовые понятия"):
    st.markdown("""
    * **ДНК (Нуклеотиды):** Строится из нуклеотидов **A** (Аденин), **T** (Тимин), **G** (Гуанин), **C** (Цитозин).
    * **мРНК:** Матричная РНК, где тимин (**T**) заменяется на урацил (**U**).
    * **Кодон:** Тройка нуклеотидов (триплет), кодирующая одну аминокислоту.
    * **Белок:** Цепочка аминокислот, определяющая структуру и функции организма.
    """)

with st.sidebar.expander("⚠️  2. Что такое мутации?"):
    st.markdown("""
    **Мутация** — это изменение в нуклеотидной последовательности ДНК:
    * **Замена нуклеотида (SNP):** Один нуклеотид заменяется другим.
    * **Синонимичная мутация:** Кодон изменился, но аминокислота осталась той же (благодаря избыточности генетического кода).
    * **Нонсенс / Миссенс:** Изменяется белковая цепь или появляется стоп-кодон, что может нарушить работу белка.
    """)

# --- ОСНОВНЫЙ ИНТЕРФЕЙС ---
st.title("🧬  Анализатор ДНК, Трансляция и Поиск Мутаций")
st.write("Сервис для трансляции последовательностей и анализа генных мутаций.")

# --- ТУТОРИАЛ / ОБУЧАЮЩИЙ ГИД ДЛЯ ВХОДА ---
with st.popover("🚀  Быстрый старт / Инструкция"):
    st.subheader("Как пользоваться сервисом?")
    st.markdown("""
    1. **Введение данных:** Введите исходную цепь ДНК в левое поле и мутировавшую в правое (используйте буквы A, T, G, C).
    2. **Запуск:** Нажмите кнопку **«Запустить биоинформатический анализ»**.
    3. **Анализ результатов:**
       * Раздел **1** покажет транскрипцию в мРНК и построение аминокислотной цепи белка.
       * Раздел **2** найдет точные позиции точечных мутаций и сформирует сводную таблицу.
    4. **Теория:** Пользуйтесь меню слева для повторения биологической базы!
    """)

st.markdown("---")

# Таблица генетического кода (кодоны -> аминокислоты)
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

# Ввод последовательностей
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
21:54


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
