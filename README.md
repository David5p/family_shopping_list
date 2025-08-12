<p>
  <img src="assets/images/start_up.png" alt="Program start up">
</p>

## Table of Contents

1. <details open>
     <summary><a href="#about">About</a></summary>

   <a href="https://github.com/David5p/family_shopping_list">Family Shopping List</a> project is a program designed for parents or guardians to create a food shopping list for the family.

   Users of the program are invited to choose from a list of options. The primary goal leads to the creation of a shopping list for either 2 or 7 days depending on the user's choice.

    <p>
        <img src="assets/images/shopping_list_choice.png" alt="Options for shopping list">
    </p>
    
    Other avenues the user can change include the respective stock and recipes list.

   </details>

2. <details open>
     <summary>User Experience</summary>
     <ul>
       <li>
         <details>
           <summary>Goals</summary>
           <ul>
             <li><a href="#visitor-goals">Visitor Goals</a></li>
             <li><a href="#business-goals">Business Goals</a></li>
             <li><a href="#user-stories">User Stories</a></li>
           </ul>
         </details>
       </li>
       <li>
         <details>
           <summary>Visual Design</summary>
           <ul>
             <li><a href="#project-board">Project Board</a></li>
             <li><a href="#fonts">Fonts</a></li>
             <li><a href="#colors">Colors</a></li>
           </ul>
         </details>
       </li>
     </ul>
   </details>

3. <details open>
     <summary>Features</summary>
     <ul>
       <li>
         <details>
           <summary>Page Elements</summary>
           <ul>
             <li><a href="#View Recipes">View Recipes</a></li>
             <li><a href="#Edit Recipes">Edit Recipes</a></li>
             <li><a href="#Generate Shopping List">Generate Shopping List</a></li>
             <li><a href="#View Stock">View Stock</a></li>
             <li><a href="#Edit Stock">Edit Stock</a></li>
             <li><a href="#Exit">Exit</a></li>
           </ul>
         </details>
       </li>
       <li>
         <details open>
           <summary>Technologies Used</summary>
           <ul>
             <li><a href="#languages">Languages</a></li>
             <li><a href="#frameworks">Frameworks</a></li>
             <li><a href="#libraries">Libraries</a></li>
             <li><a href="#platforms">Platforms</a></li>
             <li><a href="#other-tools">Other Tools</a></li>
           </ul>
         </details>
       </li>
     </ul>
   </details>

4. <details open>
     <summary>Testing</summary>
     <ul>
       <li>
         <details>
           <summary>Methods</summary>
           <ul>
             <li><a href="#validation">Validation</a></li>
             <li><a href="#general-testing">General Testing</a></li>
             <li><a href="#Flake8">Flake8</a></li>
           </ul>
         </details>
       </li>
       <li>
         <details>
           <summary>Bugs</summary>
           <ul>
             <li><a href="#known-and-fixed-bugs">Known and Fixed Bugs</a></li>
           </ul>
         </details>
       </li>
     </ul>
   </details>

5. <details open>
     <summary>Deployment</summary>
     <ul>
       <li><a href="#deployment">Deployment Details</a></li>
     </ul>
   </details>

6. <details open>
     <summary>Credit</summary>
     <ul>
       <li><a href="#content">Content</a></li>
     </ul>
   </details>

---

# User Experience (UX)

## Goals

### Visitor Goals

The target audience for the program:

- Parents or guardians looking to plan meals.
- Any adult wanting to plan their meals.
- Students or educators looking to develop an understaning of Python concepts

User goals are:

- To generate a shopping list.
- View and change stock list.
- View and change recipes list

The Capitals and Countries quiz fulfills these needs by:

- Users are prompted of their requirements to generate the shopping list.
- Users can choose to edit, remove or add stock items.
- Users can choose to edit, remove or add recipes.

### Business Goals

The Business Goals of The Capitals and Countries Quiz are:

- To save the user time by generating accurate and personalized shopping lists.
- To reduce the stress of meal planning and shopping.
- To have the potential to reduce household waste through accurate updating of stock list and following the meal plan.

### User Stories

1. As a family member, when using the command line navigation, I need a clear system which flows in the terminal and does not break down. I want to be guided through menu options clearly, so that I can update the food stock and create a shopping list without needing technical skills.

2. As a user, I want the program to tell me what to buy based on current stock and provided meal plan, So that I don’t forget anything when shopping.

3. As a user, I want to see what food items I currently have in stock, so that I can plan meals more effectively.

4. As a user, I want to reduce quantities or delete expired items from my stock, so that the data remains accurate.

5. As a user, I want to add new recipes or change existing ones, so that my meal plan is personalized.

6. As a user, I want to assign meals to specific days, so I can plan the week more precisely.

7. As a user, I want to save my weekly meal plans, so I can reuse or review them later.

## Visual Design

### Project Board

- I used the projects board to help me plan my program. I have found it a useful check guide since it was introduced and have decided to continue using it on my projects.
- The plan allowed me to focus on achieving what was most important to achieve in my program first before attempting to achieve other features.
- For example, I was able to focus on allowing the user to view recipes and stock lists and generate the shopping list before taking the development of the program further.
- It is also a useful tool to see how I could develop my program in the future or without time constraints.

### Colors

<p align="center">
  <img src="assets/images/read_me/color_palette.png" alt="color choices">
</p>

- I picked the colors (image above is a screenshot taken from <a href="https://coolors.co/">Coolors</a>) of the website from the hero image using an <a href="https://imagecolorpicker.com/">image color picker</a> tool to help me with my choices.

<p align="center">
  <img src="assets/images/read_me/main_image_colors.png" alt="color choices chosen from main image">
</p>

- I varied some of the shades recommended by the image color picker so my website had sufficient contrast.
- Colors were tested to ensure WCAG AA-level contrast compliance using WebAIM's checker.

<p align="center">
  <img src="assets/images/read_me/color_checker.png" alt="background color against question container background">
</p>
- The midnight green was quite a dark background choice and the color picker from image resulted in lighter shade recommendation. However, It was neither a dark nor light background and it proved problematic to match other colors with it whilst maintaining a good contrast level.
- This resulted in my other color choices needing to be sufficiently bright to give a good contrast level.

<p align="center">
  <img src="assets/images/read_me/color_checker1.png" alt="background color against answer buttons background">
</p>
- The midnight green background provides a great backdrop for the lighter colors of ash grey and khaki.
- Text for the question and answer options are black and bold against their lighter background choices.
- When the user answers the question, the question and answer options seemlessly change background color depending on the user's answer and the text color changes to white to reflect the changed darker backgrounds.
- White was chosen for the main-headings as it stands out against the midnight green background color
