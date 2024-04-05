import streamlit as st

registration_numbers = (
    "KAA051O",
    "KAA379O",
    "KAA433Z",
    "KAA462T",
    "KAA644N",
    "KAA764X",
    "KAA782V",
    "KAA852S",
    "KAB500V",
    "KAY023W",
    "KBA005W",
    "KBA013K",
    "KBA089K",
    "KBA127Q",
    "KBA157B",
    "KBA186S",
    "KBA226A",
    "KBA279B",
    "KBA304E",
    "KBA346K",
    "KBA485F",
    "KBA546D",
    "KBA571U",
    "KBA572Y",
    "KBA686P",
    "KBA742B",
    "KBA806Z",
    "KBA899T",
    "KBA922Q",
    "KBG178R",
    "KBJ894H",
    "KBM957Z",
    "KBN690T",
    "KBQ805S",
    "KBQ848C",
    "KBR695P",
    "KBW388H",
    "KBX197P",
    "KBX354F",
    "KBY242N",
    "KCA104D",
    "KCA157H",
    "KCA445W",
    "KCA486M",
    "KCA633B",
    "KCA636M",
    "KCA738P",
    "KCA882P",
    "KCA964Y",
    "KCC260J",
    "KCC395W",
    "KCF142V",
    "KCG108T",
    "KCG528W",
    "KCG900V",
    "KCG967T",
    "KCH003S",
    "KCH019Z",
    "KCH096Z",
    "KCJ674A",
    "KCK985E",
    "KCL363D",
    "KCM536X",
    "KCN068H",
    "KCN140V",
    "KCN854Y",
    "KCP938J",
    "KCQ910T",
    "KCR476H",
    "KCR588V",
    "KCR942T",
    "KCR999G",
    "KCS439V",
    "KCS505X",
    "KCT420Q",
    "KCU815E",
    "KCU851F",
    "KCV691R",
    "KCX522F",
    "KCX659Z",
    "KCZ156E",
    "KDA004D",
    "KDA060J",
    "KDA110A",
    "KDA142E",
    "KDA216A",
    "KDA363N",
    "KDA397O",
    "KDA419W",
    "KDA472T",
    "KDA488H",
    "KDA631Y",
    "KDA681G",
    "KDA770E",
    "KDA904U",
    "KDC544S",
    "KDH315E",
    "KDJ532B",
    "KDJ971W",
    "KDK866X",
    "KDL194E",
    "KDM331E",
    "KDM764W",
    "KDN224N",
)
# list of registration numbers

# reg_no_input = st.text_input("Enter registration number", "KAA051O")


def reg_no_input(subheader, key_suffix):
    st.subheader(subheader)

    # Add radio buttons to choose between entering or selecting a registration number
    input_method = st.radio(
        "Choose input method:",
        ("Select from list", "Enter manually"),
        key=f"input_method_{key_suffix}",
    )

    if input_method == "Select from list":
        selected_reg = st.selectbox(
            "Select a registration number",
            registration_numbers,
            key=f"selected_reg_{key_suffix}",
        )
        st.write(f"You selected registration number {selected_reg} :thumbsup:")
        return selected_reg
    else:
        given_reg = (
            st.text_input("Enter registration number", key=f"reg_no_{key_suffix}")
            .upper()
            .strip()
        )
        if given_reg in registration_numbers:
            st.write(f"Registration number {given_reg} is valid :thumbsup:")
            return given_reg
        else:
            st.write(
                f"Registration number {given_reg} is invalid. Please enter a license plate from the list."
            )
            return None
