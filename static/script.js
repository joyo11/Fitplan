document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("workoutForm");
    const resultsDiv = document.getElementById("results");
    const suggestionsDiv = document.getElementById("suggestions");
    const workoutInput = document.getElementById("workout_input");
  
    const suggestions = [
      "Cardio",
      "Build Muscle",
      "Yoga",
      "HIIT",
      "Flexibility",
      "Strength Training"
    ];
  
    // Display suggestions when typing
    workoutInput.addEventListener("input", () => {
      const query = workoutInput.value.toLowerCase();
      suggestionsDiv.innerHTML = "";
        
      if (query) {
        suggestions
          .filter(suggestion => suggestion.toLowerCase().includes(query))
          .forEach(suggestion => {
            const suggestionItem = document.createElement("div");
            suggestionItem.textContent = suggestion;
            suggestionItem.className = "suggestion-item";
            suggestionItem.addEventListener("click", () => {
              workoutInput.value = suggestion;
              suggestionsDiv.innerHTML = "";
            });
            suggestionsDiv.appendChild(suggestionItem);
          });
      }
    });
  
    // Submit the form
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      resultsDiv.innerHTML = "Generating your workout plan...";
      const workoutType = workoutInput.value;
  
      try {
        const response = await fetch("/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ workout_type: workoutType })
        });
        const data = await response.json();
  
        if (data.success) {
          resultsDiv.innerHTML = `<h3>Workout Plan</h3><p>${data.workout}</p>`;
        } else {
          resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        }
      } catch (error) {
        resultsDiv.innerHTML = `<p>Something went wrong. Please try again later.</p>`;
      }
    });
  });
  
