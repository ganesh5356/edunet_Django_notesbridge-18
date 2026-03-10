const chatKnowledge = {
    "project": "NotesBridge is a Senior-to-Junior Learning Network that centralizes study materials like Notes, Books, NPTEL, and Previous Papers.",
    "notesbridge": "NotesBridge is a platform designed to connect Seniors and Juniors for knowledge sharing through study materials.",
    "notes": "You can find and search for various study materials like Notes, Books, and Papers in the Resources section.",
    "study": "We provide centralized study materials including Notes, Books, NPTEL resources, and Previous Papers.",
    "books": "Our library includes various books categorized by subject and semester in the Resources section.",
    "senior": "Seniors are mentors who can upload study materials to help their juniors learn efficiently.",
    "junior": "Juniors can search for, view, and learn from resources shared by experienced Seniors.",
    "upload": "Only users with the 'Senior' role can upload new resources to the platform.",
    "role": "Roles (Junior or Senior) are chosen during signup and determine your permissions on the site.",
    "signup": "Create an account by clicking 'Sign Up'. You'll need to choose if you are a Junior or a Senior.",
    "login": "Use the 'Login' page to access your account with your username and password.",
    "signin": "Click 'Login' in the navigation bar to access your NotesBridge account.",
    "logout": "You can end your session by clicking 'Logout' in the top navigation bar.",
    "nptel": "We host NPTEL study materials and links to help you with your specialized courses.",
    "papers": "Previous year question papers and model answers are available in the Resources section.",
    "about": "NotesBridge aims to empower students through collaborative peer learning and easy access to materials.",
    "help": "I can assist you with questions about NotesBridge features, roles, and navigation. Ask me about notes, roles, or how to join!",
    "contact": "You can reach out to us at info@notesbridge.com for any specific support queries.",
    "download": "You can download resources by clicking on the download button in the resource card.",
    "bookmark": "You can bookmark resources by clicking on the bookmark button in the resource card.",
    "remove-bookmark": "You can remove bookmarks by clicking on the bookmark button in the resource card.",
    "dashboard": "You can view and search for resources in the dashboard.",
    "resources": "You can view and search for resources in the resources section.",
    "doubts": "You can view and search for doubts in the doubts section.",
    "upload": "You can upload resources by clicking on the upload button in the resources section.",
    "profile": "You can view and edit your profile in the profile section.",
    "edit-profile": "You can view and edit your profile in the profile section.",
    "bookmarks": "You can view your bookmarks in the bookmarks section.",


};

function getChatResponse(query) {
    const lowerQuery = query.toLowerCase();

    for (const key in chatKnowledge) {
        if (lowerQuery.includes(key)) {
            return chatKnowledge[key];
        }
    }

    return "I don't know, ask only about project.";
}
