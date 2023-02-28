// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyC5FmgOD2It3sF_8xn8fayVr1KiNP9E56I",
  authDomain: "react-auth-posege.firebaseapp.com",
  projectId: "react-auth-posege",
  storageBucket: "react-auth-posege.appspot.com",
  messagingSenderId: "622186110418",
  appId: "1:622186110418:web:704331dd41c048aff9fc0b",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// export const auth = firebase.auth();
// export const firestore = firebase.firestore();
