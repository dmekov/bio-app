import streamlit as st
import pandas as pd

st.set_page_config(page_title="Анализ Мутаций ДНК", layout="wide", page_icon="🧬 ")

# --- ВЫБОР РЕЖИМА ПОЛЬЗОВАТЕЛЯ ---
st.sidebar.title("⚙️  Настройки режима")
mode = st.sidebar.radio(
    "Выберите уровень подготовки:",
    ["🌱  Начинающий (Простыми словами)", "🔬  Продвинутый (Научный биоинформатик)"]
)

is_advanced = "Продвинутый" in mode

# --- БОКОВАЯ ПАНЕЛЬ: СПРАВОЧНИК В ЗАВИСИМОСТИ ОТ РЕЖИМА ---
st.sidebar.markdown("---")
st.sidebar.title("📚 Справочник")

if not is_advanced:
    st.sidebar.info("💡  **Главный принцип:** ДНК — это как кулинарная книга, а Белок — готовое блюдо.")
    st.sidebar.markdown("""
    **Простые понятия:**
    * **Буквы ДНК (A, T, G, C):** Символы, из которых состоит инструкция организма.
    * **Замена буковки:** Представь опечатку в слове — она может изменить весь смысл предложения!
    * **Белок:** Строительный материал нашего тела (мышцы, ферменты, кожа).
    """, help="Наводите на термины для подсказок!")
else:
    st.sidebar.info("🔬  **Центральная догма:** ДНК ➔ мРНК ➔ Белок")
    st.sidebar.markdown("""
    **Биоинформатические термины:**
    * **Транскрипция:** Синтез мРНК по матрице ДНК (T ➔ U).
    * **Трансляция:** Декодирование триплетов (кодонов) в аминокислоты.
    * **SNP (Точечный полиморфизм):** Мутация замены одного нуклеотида.
    * **Синонимичность:** Несколько кодонов могут кодировать одну аминокислоту.
    """, help="Наводите на термины для подробностей!")

# --- ОСНОВНОЙ ЗАГОЛОВОК И ТУТОРИАЛ ---
if is_advanced:
    st.title("🔬  Анализатор Генома: Трансляция и Мутационный Анализ")
    st.caption("Профессиональный модуль сравнения нуклеотидных последовательностей и экспрессии белков.")
else:
    st.title("🌱  Занимательная ДНК: Поисковик Опечаток в Генах")
    st.caption("Простой сервис, который поможет понять, как небольшая ошибка в ДНК меняет организмы.")

# Переключаемый туториал
with st.expander("❓ Как этим пользоваться? (Нажмите, чтобы развернуть/скрыть)", expanded=True):
    if not is_advanced:
        st.write("""
        1. Введи 'исходную' цепочку ДНК и 'мутировавшую' (с ошибкой).
        2. Нажми большую кнопку внизу.
        3. Мы покажем, как эти буквы превращаются в цепочку белка и где именно закралась опечатка!
        """)
    else:
        st.write("""
        1. Введите матричную цепь ДНК (5'-3') в левое и правое поля.
        2. Инициализируйте биоинформатический скрипт обработки.
        3. Система выполнит матричную транскрипцию в мРНК, транслирует полипептид и локализует позицию SNP.
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
    label_orig = "Исходная цепочка ДНК:" if not is_advanced else "Матричная цепь ДНК (Wild Type):"
    dna_input = st.text_area(label_orig, "ATGCGATCGATCGTTTAG").upper().strip()

with col2:
    label_mut = "Цепочка ДНК с ошибкой (мутацией):" if not is_advanced else "Мутантная цепь ДНК (Mutant Type):"
    mutated_dna = st.text_area(label_mut, "ATGCGACCGATCGTTTAG").upper().strip()
    btn_text = "🚀  Сравнить и найти ошибки" if not is_advanced else "🧬  Запустить геномный анализ"

if st.button(btn_text):
    rna = dna_to_rna(dna_input)
    protein_orig = translate_dna(dna_input)
    protein_mut = translate_dna(mutated_dna)
    
    st.markdown("---")
    
    if not is_advanced:
        st.subheader("1. Перевод букв ДНК в белок")
        st.write("Сначала ДНК переписывается в рабочую копию (РНК), а затем сборщик собирает из неё белок:")
    else:
        st.subheader("1. Результаты транскрипции и трансляции")
        st.write("Синтез мРНК и первичной структуры полипептидной цепи:")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.write("**Копия для сборки (мРНК - Исходная):**" if not is_advanced else "**мРНК (Wild Type):**")
        st.code(rna)
        st.write("**Готовый белок (Исходный):**" if not is_advanced else "**Полипептид (Wild Type):**")
        st.code(protein_orig)
        
    with res_col2:
        st.write("**Копия для сборки (мРНК - Измененная):**" if not is_advanced else "**мРНК (Mutant Type):**")
        st.code(dna_to_rna(mutated_dna))
        st.write("**Готовый белок (Измененный):**" if not is_advanced else "**Полипептид (Mutant Type):**")
        st.code(protein_mut)
        
    st.markdown("---")
    
    if not is_advanced:
        st.subheader("2. Где закралась ошибка (мутация)?")
    else:
        st.subheader("2. Локализация точечных мутаций (SNP)")
    
    min_len = min(len(dna_input), len(mutated_dna))
    mutations = []
    
    for idx in range(min_len):
        if dna_input[idx] != mutated_dna[idx]:
            mutations.append({
                "Номер буквы": idx + 1,
                "Было в норме": dna_input[idx],
                "Стало при ошибке": mutated_dna[idx]
            })
            
    if mutations:
        if not is_advanced:
            st.warning(f"Найдено опечаток: {len(mutations)}")
            st.write("Вот на каких позициях буквы отличаются:")
        else:
            st.warning(f"Выявлено нуклеотидных замен (SNP): {len(mutations)}")
        st.table(pd.DataFrame(mutations))
    else:
        st.success("Ошибок не найдено! Обе цепочки полностью одинаковые." if not is_advanced else "Последовательности идентичны. Точечные мутации отсутствуют.")
