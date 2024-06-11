 document.addEventListener("DOMContentLoaded", function () {
   // Toggle the mobile menu
   const mobileMenuButton = document.querySelector(
     '[aria-controls="mobile-menu"]'
   );
   const mobileMenu = document.getElementById("mobile-menu");

   mobileMenuButton.addEventListener("click", function () {
     const expanded =
       mobileMenuButton.getAttribute("aria-expanded") === "true" || false;
     mobileMenuButton.setAttribute("aria-expanded", !expanded);
     mobileMenu.classList.toggle("hidden");
   });

   // Toggle the user menu
   const userMenuButton = document.getElementById("user-menu-button");
   const userMenu = document.getElementById("user-menu");

   userMenuButton.addEventListener("click", function () {
     const expanded =
       userMenuButton.getAttribute("aria-expanded") === "true" || false;
     userMenuButton.setAttribute("aria-expanded", !expanded);
     userMenu.classList.toggle("hidden");
   });

   // Toggle the small navigation menu
   const smallNavButton = document.getElementById("small-nav-button");
   const smallNavMenu = document.getElementById("small-nav-menu");

   smallNavButton.addEventListener("click", function () {
     smallNavMenu.classList.toggle("hidden");
   });
 });
