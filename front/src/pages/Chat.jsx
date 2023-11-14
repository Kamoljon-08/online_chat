import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { io } from "socket.io-client";
import styled from "styled-components";
import { allUsersRoute } from "../utils/APIRoutes";
import ChatContainer from "../components/ChatContainer";
import Contacts from "../components/Contacts";
import Welcome from "../components/Welcome";

export default function Chat() {
  const socket = useRef();
  const [contacts, setContacts] = useState([]);
  const [currentChat, setCurrentChat] = useState(undefined);
  const [localhostKey, setLocalhostKey] = useState(JSON.parse(localStorage.getItem(process.env.REACT_APP_LOCALHOST_KEY)))
  
  useEffect(() => {
    setLocalhostKey(JSON.parse(localStorage.getItem(process.env.REACT_APP_LOCALHOST_KEY)))
  }, [])
  
  useEffect(() => {
    if (localhostKey) {
      socket.current = io("https://online-chat-ten.vercel.app/");
      socket.current.emit("add-user", localhostKey.user?.id);
    }
  }, [localhostKey])

  useEffect(() => {
    axios.get(`${allUsersRoute}`).then(res => setContacts(res.data))
  }, []);
  const handleChatChange = (chat) => {
    setCurrentChat(chat);
  };
  return (
    <>
      <Container>
        <div className="container">
          <Contacts contacts={contacts} changeChat={handleChatChange} />
          {currentChat === undefined ? (
            <Welcome />
          ) : (
            <ChatContainer currentChat={currentChat} socket={socket} />
          )}
        </div>
      </Container>
    </>
  );
}

const Container = styled.div`
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  align-items: center;
  background-color: #131324;
  .container {
    height: 85vh;
    width: 85vw;
    background-color: #00000076;
    display: grid;
    grid-template-columns: 25% 75%;
    @media screen and (min-width: 720px) and (max-width: 1080px) {
      grid-template-columns: 35% 65%;
    }
  }
`;
