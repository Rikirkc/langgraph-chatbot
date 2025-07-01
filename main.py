import streamlit as st
import datetime
from langchain_core.messages import HumanMessage, AIMessage
from chatbot.graph import create_chatbot_graph
from chatbot.pdf_generator import generate_pdf_report

st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="wide")

# Initialize session state variables 
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_message_count' not in st.session_state:
    st.session_state.user_message_count = 0
if 'conversation_ended' not in st.session_state:
    st.session_state.conversation_ended = False
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = f"conversation_{datetime.datetime.now().timestamp()}"

def main():
    st.title("🤖 LangGraph Chatbot with Memory")
    st.markdown("---")

    with st.sidebar:
        st.markdown("### Conversation Info")
        st.info(f"Messages sent: {st.session_state.user_message_count}/5")

        if st.session_state.conversation_ended:
            st.warning("Conversation ended - Max messages reached")

        if st.button("🔄 Reset Conversation"):
            st.session_state.messages = []
            st.session_state.user_message_count = 0
            st.session_state.conversation_ended = False
            st.session_state.graph = None
            st.session_state.thread_id = f"conversation_{datetime.datetime.now().timestamp()}"
            st.rerun()

    # Initializing the graph
    if st.session_state.graph is None:
        try:
            st.session_state.graph = create_chatbot_graph()
            st.success("Chatbot initialized successfully!")
        except Exception as e:
            st.error(f"Graph init error: {str(e)}")
            return

    # Display past messages
    for msg in st.session_state.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # User input is taken from here
    if not st.session_state.conversation_ended:
        if prompt := st.chat_input("What would you like to talk about?"):
            user_msg = HumanMessage(content=prompt)
            st.session_state.messages.append(user_msg)

            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                state = {
                    "messages": st.session_state.messages,
                    "user_count": st.session_state.user_message_count + 1
                }

                result = st.session_state.graph.invoke(state, config={"configurable": {"thread_id": st.session_state.thread_id}})
                st.session_state.messages = result["messages"]
                st.session_state.user_message_count = result["user_count"]

                if st.session_state.user_message_count >= 5:
                    st.session_state.conversation_ended = True

                latest_ai_msg = [m for m in result["messages"] if isinstance(m, AIMessage)][-1]
                with st.chat_message("assistant"):
                    st.markdown(latest_ai_msg.content)

                st.rerun()

            except Exception as e:
                st.error(f"Bot error: {str(e)}")
    else:
        st.info("Chat ended. Download the PDF summary below or reset to restart.")

    # Pdf generation block
    if st.session_state.messages:
        st.markdown("---")
        st.subheader("📄 Conversation Summary")
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("📥 Generate & Download PDF Report", type="primary"):
                try:
                    pdf = generate_pdf_report(st.session_state.messages, st.session_state.user_message_count)
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf.getvalue(),
                        file_name=f"conversation_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        type="secondary"
                    )
                    st.success("PDF report generated!")
                except Exception as e:
                    st.error(f"PDF error: {str(e)}")

        with col2:
            st.metric("Total Messages", len(st.session_state.messages))
            st.metric("User Messages", st.session_state.user_message_count)

if __name__ == "__main__":
    main()
