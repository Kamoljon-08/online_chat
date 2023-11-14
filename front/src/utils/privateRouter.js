import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const PrivateRouter = ({ children }) => {
  let Usertoken = localStorage.getItem(process.env.REACT_APP_LOCALHOST_KEY);
  const navigate = useNavigate();

  useEffect(() => {
   
    setTimeout(() => {
        if (!Usertoken) navigate("/login");
    }, 2000)
  }, [Usertoken, navigate]);

 

  return children;
};

export default PrivateRouter;