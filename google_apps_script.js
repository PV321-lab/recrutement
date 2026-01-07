/**
 * Script Google Apps pour envoyer des emails via une requête POST.
 * Déployez ce script en tant qu'application Web avec accès "Tout le monde".
 */

function doPost(e) {
  try {
    // Récupération des paramètres de la requête
    var to = e.parameter.to;
    var subject = e.parameter.subject;
    var body = e.parameter.body;
    var from = e.parameter.from;
    var password = e.parameter.password; // Note: Le mot de passe n'est pas utilisé par GmailApp car il utilise l'identité du script

    if (!to || !subject || !body) {
      return ContentService.createTextOutput(JSON.stringify({
        "success": false,
        "error": "Paramètres manquants (to, subject, body)"
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Envoi de l'email via le service Gmail de Google Apps Script
    // L'email sera envoyé depuis l'adresse du compte Google qui a déployé le script
    GmailApp.sendEmail(to, subject, body);

    return ContentService.createTextOutput(JSON.stringify({
      "success": true,
      "message": "Email envoyé avec succès"
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      "success": false,
      "error": error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("Le script est opérationnel. Utilisez POST pour envoyer des emails.");
}
