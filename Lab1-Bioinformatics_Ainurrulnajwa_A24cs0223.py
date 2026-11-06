from Bio import Entrez
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import streamlit as st


Entrez.email = "Intannurlayla564@yahoo.com"


def retrieve_data(protein_id):
    handle = Entrez.efetch(db='protein', id=protein_id, rettype='fasta')
    record = SeqIO.read(handle, 'fasta')
    handle.close()
    return record


def get_basic_analysis(sequence):
   
    seq_str = str(sequence)
    
    length = len(seq_str)
    
    seq_analysis = ProteinAnalysis(seq_str)
    
    aa_comp = seq_analysis.count_amino_acids()
    mw = seq_analysis.molecular_weight()
    pI = seq_analysis.isoelectric_point()
    
   
    return length, aa_comp, mw, pI




st.title('Lab 1 - Lab Bioinformatic 2')

protein_id = st.text_input('Enter Uniprot ID', value='P04637')
retrieve = st.button('Retrieve')

if retrieve:
    if protein_id != "":
        try:
            with st.spinner('taking data'):
                record = retrieve_data(protein_id)
                length, aa_comp, mw, pI = get_basic_analysis(record.seq)

            st.success('data retrieved successfully')

            st.subheader("📌 Basic Information")
            st.text(f"ID: {record.id}")
            st.text(f"Name: {record.name}")
            st.text(f"Description: {record.description}")
            
            st.subheader("🧬 Protein Sequence")
            st.code(str(record.seq))

            st.subheader("📊 Basic Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Sequence Length", f"{length} aa")
            col2.metric("Molecular Weight", f"{mw:.2f} Da")
            col3.metric("Isoelectric Point (pI)", f"{pI:.2f}")

            st.write("**Amino Acid Composition:**")
            st.json(aa_comp)

        except Exception as e:
            st.error(f"error occurred: {e}")
            st.info("please ensure the ID is valid (contoh: P04637).")
    else:
        st.warning('Please enter Uniprot ID')