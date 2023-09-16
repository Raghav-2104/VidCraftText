import { initializeApp } from 'firebase/app';
const firebaseConfig = {
    apiKey: "AIzaSyC9iv8tKAM0IJehmc4FE7h8rO1J_EzlmUo",
    authDomain: "sih23-daf87.firebaseapp.com",
    projectId: "sih23-daf87",
    storageBucket: "sih23-daf87.appspot.com",
    messagingSenderId: "914927194887",
    appId: "1:914927194887:web:04cec8f7f73feb0ea5eba2"
};
const app = initializeApp(firebaseConfig);

function signUp() {
    var email = document.getElementById("upemail");
    var password = document.getElementById("uppassword");

    const promise = auth.createUserWithEmailAndPassword(email.value, password.value);
    promise.catch(e => alert(e.message));

    alert("Signed Up");
}

function signIn(){
    var email = document.getElementById("inemail");
    var password = document.getElementById("inpassword");

    const promise = auth.signInWithEmailAndPassword(email.value, password.value);
    promise.catch(e => alert(e.message));

    alert("Signed In" + email.value);
}
//print current user
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // User logged in already or has just logged in.
        console.log(user);
    } else {
        // User not logged in or has just logged out.
    }
});