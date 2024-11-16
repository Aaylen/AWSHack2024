// firebaseConfig.js
import firebase from "firebase/compat/app";
import "firebase/compat/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAljJa_na2oGDaDEHZGDTrPvHeLR4bOTwU",
    authDomain: "profitpilot-hackathon.firebaseapp.com",
    projectId: "profitpilot-hackathon",
    storageBucket: "profitpilot-hackathon.firebasestorage.app",
    messagingSenderId: "422218758234",
    appId: "1:422218758234:web:cd34871ea9bdbf2f5e4063"
};

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

export const auth = firebase.auth();
export const googleProvider = new firebase.auth.GoogleAuthProvider();