import React, { useState, useEffect } from "react";
import styled from "styled-components";
import Robot from "../assets/robot.gif";
export default function Welcome() {
  const [localhostKey, setLocalhostKey] = useState(JSON.parse(localStorage.getItem(process.env.REACT_APP_LOCALHOST_KEY)))

  useEffect(() => {
    setLocalhostKey(JSON.parse(localStorage.getItem(process.env.REACT_APP_LOCALHOST_KEY)))
  }, [])
  return (
    <Container>
      <img src={Robot} alt="" />
      <h1>
        Welcome, <span>{localhostKey?.user?.userName}!</span>
      </h1>
      <h3>Please select a chat to Start messaging.</h3>
    </Container>
  );
}

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  flex-direction: column;
  img {
    height: 20rem;
  }
  span {
    color: #4e0eff;
  }
`;
