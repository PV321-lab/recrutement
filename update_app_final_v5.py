import re

def update_code(content):
    # 1. Scripts - Ensure correct order and compat versions
    content = content.replace(
        '<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-database-compat.js"></script>',
        '<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-database-compat.js"></script>\n  <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>'
    )
    
    # 2. Config & Init - Use a clean block
    config_init = """
  const firebaseConfig = {
    apiKey: "AIzaSyDbJe_e0Uz5YavmQDwabym11FStEPjxo2E",
    authDomain: "invitedb-6ce9f.firebaseapp.com",
    databaseURL: "https://invitedb-6ce9f-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "invitedb-6ce9f",
    storageBucket: "invitedb-6ce9f.firebasestorage.app",
    messagingSenderId: "253833375693",
    appId: "1:253833375693:web:a1d68bef41916c86be5e84",
    measurementId: "G-BS2EBMM7T3"
  };
  
  // Initialisation Firebase
  try {
    if (!firebase.apps.length) {
      firebase.initializeApp(firebaseConfig);
    }
  } catch (e) {
    console.error("Firebase Init Error:", e);
  }
  const database = firebase.database();
  const AUTH_EMAIL = "maraminho10@gmail.com";
  const AUTH_PASS = "M@ra10";
"""
    # Replace everything from config to database init
    content = re.sub(r'const firebaseConfig = \{.*?\};.*?const database = firebase\.database\(\);', config_init, content, flags=re.DOTALL)

    # 3. Fix Syntax Error in PDF Rules (the smart quotes issue)
    content = content.replace("1. Si vous êtes Couples marocains:’,", "1. Si vous êtes Couples marocains:',")
    content = content.replace("1. Si vous êtes des Couples marocains:',", "1. Si vous êtes des Couples marocains:',")

    # 4. Correct Login Logic
    login_logic = """
  async function login(){
    hideInlineMsg('loginMsg');
    const u = document.getElementById('loginUser').value.trim();
    const p = document.getElementById('loginPass').value.trim();

    if(!u || !p){
      showInlineMsg('loginMsg','err',"Saisissez l'utilisateur et le mot de passe.");
      return;
    }

    const btn = document.getElementById('btnLogin');
    btn.disabled = true;
    btn.textContent = "Connexion...";

    try {
      // 1. Priorité Admin/Admin
      if(u === 'admin' && p === 'admin'){
        // Authentification Firebase en arrière-plan pour l'admin
        try {
          await firebase.auth().signInWithEmailAndPassword(AUTH_EMAIL, AUTH_PASS);
        } catch (e) {
          console.error("Firebase Auth failed for admin:", e);
        }
        
        currentUser = { role:'admin' };
        document.getElementById('loginCard').classList.add('hidden');
        document.getElementById('adminPanel').classList.remove('hidden');
        document.getElementById('documentColumn').classList.remove('hidden');
        showBanner('ok', "Connecté en tant qu'administrateur.");
        startSessionTimer();
        refreshAdmin();
        return;
      }

      // 2. Authentification Firebase pour les autres utilisateurs
      await firebase.auth().signInWithEmailAndPassword(AUTH_EMAIL, AUTH_PASS);

      // 3. Recherche de l'utilisateur dans la base de données
      const snapshot = await database.ref('users/' + u).once('value');
      const user = snapshot.val();
      
      if(user && user.pass === p){
        currentUser = { role:'user', id:u, appart:user.appart, bat:user.bat };
        
        const settingsSnapshot = await database.ref('settings/' + u).once('value');
        if(settingsSnapshot.exists()){
          userSettings = settingsSnapshot.val();
          document.getElementById('maxRecords').value = userSettings.maxRecords || 10;
        }
        
        const emailSnapshot = await database.ref('emailSettings/' + u).once('value');
        if(emailSnapshot.exists()){
          emailSettings = emailSnapshot.val();
          document.getElementById('enableEmail').value = emailSettings.enableEmail || 'non';
          toggleEmailFields();
          if(emailSettings.enableEmail === 'oui'){
            document.getElementById('userEmail').value = emailSettings.userEmail || '';
            document.getElementById('emailPassword').value = emailSettings.emailPassword || '';
            document.getElementById('guardEmail').value = emailSettings.guardEmail || '';
          }
        }
        
        document.getElementById('loginCard').classList.add('hidden');
        document.getElementById('userPanel').classList.remove('hidden');
        document.getElementById('documentColumn').classList.remove('hidden');
        showBanner('ok', `Connecté. Appartement ${user.appart} / Immeuble ${user.bat}.`);
        startSessionTimer();
        refreshUser();
      } else {
        showInlineMsg('loginMsg','err',"Identifiants incorrects.");
        await firebase.auth().signOut();
      }
    } catch (error) {
      console.error("Login Error:", error);
      showInlineMsg('loginMsg','err', "Erreur: " + (error.message || "Accès refusé"));
    } finally {
      btn.disabled = false;
      btn.textContent = "Connexion";
    }
  }
"""
    # Replace the old login function
    content = re.sub(r'async function login\(\)\{.*?\}\s+function toggleEmailFields', login_logic + '\n\n  function toggleEmailFields', content, flags=re.DOTALL)

    return content

with open('/home/ubuntu/upload/pasted_content.txt', 'r') as f:
    original_content = f.read()

clean_content = original_content.strip()
if clean_content.startswith('```html'):
    clean_content = clean_content[7:]
if clean_content.endswith('```'):
    clean_content = clean_content[:-3]

updated_content = update_code(clean_content)

with open('/home/ubuntu/app_final.html', 'w') as f:
    f.write(updated_content)
