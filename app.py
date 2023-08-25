import streamlit as st

def main():
    st.title("Hello World Streamlit App")
    st.write("Welcome to your first Streamlit app!")

    num1 = st.number_input("num1:")
    num2 = st.number_input("num2:")
    result = num1+num2
    st.write(f"The sum of {num1} and {num2} is: {result}")

    return result

if __name__ == "__main__":
    main()
