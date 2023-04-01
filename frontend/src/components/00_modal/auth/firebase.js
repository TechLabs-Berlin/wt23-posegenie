import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyC5FmgOD2It3sF_8xn8fayVr1KiNP9E56I",
  authDomain: "react-auth-posege.firebaseapp.com",
  projectId: "react-auth-posege",
  storageBucket: "react-auth-posege.appspot.com",
  messagingSenderId: "622186110418",
  appId: "1:622186110418:web:704331dd41c048aff9fc0b",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
