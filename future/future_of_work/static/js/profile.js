document.addEventListener("DOMContentLoaded", () => {

  // Copy referral button logic
  const copyBtn = document.getElementById("copy-referral-btn");
  const refText = document.getElementById("referral-text");

  if(copyBtn && refText) {
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(refText.textContent.trim());
      copyBtn.textContent = "Copied";
      setTimeout(() => copyBtn.textContent = "Copy", 1500);
    });
  }

  // Copy referred button logic
  const copyBtn1 = document.getElementById("copy-referred-btn");
  const refText1 = document.getElementById("referred-text");

  if(copyBtn1 && refText1) {
    copyBtn1.addEventListener("click", () => {
      navigator.clipboard.writeText(refText1.textContent.trim());
      copyBtn1.textContent = "Copied";
      setTimeout(() => copyBtn1.textContent = "Copy", 1500);
    });
  }

  // Profile image preview logic
  const profileInput = document.getElementById("profile_image_input");
  const previewImg = document.getElementById("profile-image-preview");
  const fileNameText = document.getElementById("selected-file-name");

  if(profileInput) {
    profileInput.addEventListener("change", (event) => {
      const file = event.target.files[0];

      if (file) {
        // Update image preview
        previewImg.src = URL.createObjectURL(file);

        // Show file name
        if(fileNameText) {
          fileNameText.textContent = file.name;
          fileNameText.classList.remove("hidden");
        }
      }
    });
  }

});
