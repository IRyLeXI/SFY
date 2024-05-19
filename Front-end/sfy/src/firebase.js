import { initializeApp } from 'firebase/app';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
    apiKey: "AIzaSyBtv-ZGWmDZrUuA91bbkLJ-FAO8pEMsFWI",
    authDomain: "sfy-firebase.firebaseapp.com",
    projectId: "sfy-firebase",
    storageBucket: "sfy-firebase.appspot.com",
    messagingSenderId: "118125074605805811554",
    appId: "1:1181250746058:web:6c52fdad9bc7bb9ddfcf72"
  };
  

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

export { storage };