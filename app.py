from flask import Flask, render_template_string
import math 

app = Flask(__name__)

# ------------------------------------------------------------------
# CSS STYLES 
# ------------------------------------------------------------------
COMMON_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Quicksand:wght@500;700&display=swap');

    body {
        background-color: #ffe6e6;
        font-family: 'Quicksand', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
        overflow: hidden;
        position: relative; 
    }

    h1 {
        font-family: 'Pacifico', cursive;
        color: #d6336c;
        font-size: 3rem;
        margin-bottom: 20px;
    }

    .btn {
        padding: 12px 25px;
        font-size: 1.2rem;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        margin: 10px;
        transition: transform 0.2s;
        font-family: 'Quicksand', sans-serif;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
    }

    .btn-primary {
        background-color: #ff4d6d;
        color: white;
        box-shadow: 0 4px 15px rgba(255, 77, 109, 0.4);
    }

    .btn-secondary {
        background-color: #fff;
        color: #ff4d6d;
        border: 2px solid #ff4d6d;
    }
    
    .btn:hover { transform: scale(1.05); }

    /* FLOATING ASSETS (HEARTS) */
    @keyframes float {
        0% { transform: translateY(0) scale(1) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100vh) scale(1.5) rotate(360deg); opacity: 0; }
    }

    .floating-asset {
        position: absolute;
        bottom: 0;
        animation: float linear infinite;
        z-index: 0; /* Default background hearts */
        pointer-events: none;
    }

    /* CSS HEART SHAPE */
    .css-heart {
        width: 15px;
        height: 15px;
        background-color: currentColor;
        transform: rotate(-45deg);
        position: relative;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .css-heart::before,
    .css-heart::after {
        content: '';
        position: absolute;
        width: 15px;
        height: 15px;
        background-color: currentColor;
        border-radius: 50%;
    }
    .css-heart::before { left: 7.5px; }
    .css-heart::after { top: -7.5px; }
</style>
"""

# ------------------------------------------------------------------
# HEART GENERATOR FUNCTIONALITY (Correct JavaScript using 'Math')
# ------------------------------------------------------------------
GENERATOR_SCRIPT = """
    // FLOATING HEART GENERATOR
    function createFloatingHeart() {
        const heartContainer = document.createElement('div');
        heartContainer.classList.add('floating-asset');
        
        const heartShape = document.createElement('div');
        heartShape.classList.add('css-heart');
        heartContainer.appendChild(heartShape);
        
        // Randomize starting position, size, and speed - Uses correct JavaScript Math object
        heartContainer.style.left = Math.random() * 100 + 'vw';
        heartContainer.style.animationDuration = (Math.random() * 8 + 6) + 's'; // 6 to 14 seconds
        heartContainer.style.animationDelay = (Math.random() * -10) + 's'; 
        heartContainer.style.color = ['#ff4d6d', '#ff85a2', '#d6336c'][Math.floor(Math.random() * 3)];
        heartShape.style.transform = `scale(${(Math.random() * 0.8 + 0.6).toFixed(2)}) rotate(-45deg)`; // Random scale for visual depth

        document.body.appendChild(heartContainer);

        setTimeout(() => heartContainer.remove(), 14000); 
    }
    
    // Start creation loop
    setInterval(createFloatingHeart, 200); // Increased frequency for MORE hearts
"""

# ------------------------------------------------------------------
# PAGE 1: THE ENVELOPE
# ------------------------------------------------------------------
PAGE_ENVELOPE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>For You</title>
    {common_style}
    <style>
        .envelope-wrapper {{
            position: relative;
            margin-top: 20px; 
        }}

        .envelope {{
            position: relative;
            width: 300px;
            height: 200px;
            background-color: #ff85a2; 
            border-radius: 0 0 10px 10px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}

        /* WIGGLE ANIMATION ON HOVER */
        @keyframes wiggle {{
            0%, 100% {{ transform: rotate(0deg); }}
            25% {{ transform: rotate(2deg); }}
            50% {{ transform: rotate(0deg); }}
            75% {{ transform: rotate(-2deg); }}
        }}

        .envelope:hover {{
            animation: wiggle 0.5s ease-in-out infinite;
            cursor: pointer;
        }}

        /* GREETING TEXT */
        .greeting {{
            font-family: 'Pacifico', cursive;
            color: #d6336c;
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 5px rgba(255, 180, 180, 0.5);
            z-index: 10;
            /* **ADDED** */
            transition: transform 0.8s ease-in-out; 
        }}

        /* **ADDED: New rule to move the greeting up when the envelope is open** */
        #greetingText.open {{
            transform: translateY(-90px);
        }}

        /* POCKET (Front Triangles) */
        .pocket {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 0;
            border-style: solid;
            border-width: 0 150px 100px 150px; 
            border-color: transparent transparent #ff9bb5 transparent;
            z-index: 3;
            border-radius: 0 0 10px 10px;
            pointer-events: none; 
        }}
        
        .pocket-sides {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 3;
            pointer-events: none;
        }}
        .pocket-sides::before {{
            content: ''; position: absolute; left: 0; bottom: 0; width: 0; height: 0;
            border-style: solid; border-width: 100px 0 100px 150px;
            border-color: transparent transparent transparent #ff85a2;
            border-radius: 0 0 0 10px;
        }}
        .pocket-sides::after {{
            content: ''; position: absolute; right: 0; bottom: 0; width: 0; height: 0;
            border-style: solid; border-width: 100px 150px 100px 0;
            border-color: transparent #ff85a2 transparent transparent;
            border-radius: 0 0 10px 0;
        }}

        /* FLAP */
        .flap {{
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 0;
            border-style: solid;
            border-width: 110px 150px 0 150px;
            border-color: #ff5c8a transparent transparent transparent;
            transform-origin: top;
            transition: transform 0.4s ease-in-out, z-index 0.4s;
            z-index: 4;
        }}
        .flap.open {{
            transform: rotateX(180deg);
            z-index: 1; 
        }}
        
        /* NEW: Clipping container for the letter */
        .letter-container {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%; 
            overflow: hidden; /* THE KEY for making it look like it's inside */
            z-index: 2; /* Below the flap (4), above the pocket (3) */
        }}

        /* SMALL LETTER (Animation now slides UP out of the container) */
        .letter-preview {{
            position: absolute;
            bottom: 0; /* Start anchored to the bottom of the clipping container */
            left: 15px;
            width: 270px;
            height: 180px; 
            background-color: #fff;
            border-radius: 5px;
            transition: transform 0.5s ease-in-out;
            
            display: flex;
            flex-direction: column;
            justify-content: flex-start; 
            align-items: center; 
            opacity: 0;
            pointer-events: none;
            padding-top: 50px; 
            
            /* Initial state: Hidden at the bottom of the container */
            transform: translateY(100%); 
        }}
        
        .letter-preview.slide-up {{
            transform: translateY(-10px); /* Move UP by 80px to peek out */
            opacity: 1;
            pointer-events: auto;
            box-shadow: 0 -5px 10px rgba(0,0,0,0.1);
        }}

        /* Z-index for peek hearts to appear IN FRONT of the envelope and flap */
        .floating-asset.peek-heart-asset {{
            z-index: 10; 
        }}


        /* FULLSCREEN OVERLAY LETTER */
        .fullscreen-letter {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(255, 230, 230, 0.95);
            z-index: 9999; 
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            backdrop-filter: blur(5px);
        }}

        .fullscreen-letter.visible {{
            opacity: 1;
            pointer-events: auto;
        }}

        .paper {{
            width: 85%;
            max-width: 500px;
            height: 85%;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transform: scale(0.8);
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-align: center;
            border: 2px solid #ffccd5;
        }}

        .fullscreen-letter.visible .paper {{
            transform: scale(1);
        }}
        
        .confession-text {{
            text-align: center; /* This centers the text lines */
            font-size: 0.8rem; 
            line-height: 1.3; 
            color: #555; 
            max-width: 90%;
            margin-top: 20px;
            margin-bottom: 20px;
        }}

        .heart-seal {{
            position: absolute; top: -55px; left: 50%; transform: translateX(-55%) rotate(45deg);
            width: 30px; height: 30px; background-color: #ff0000; z-index: 5;
        }}
        .heart-seal::before, .heart-seal::after {{
            content: ''; width: 30px; height: 30px; background-color: #ff0000;
            border-radius: 50%; position: absolute;
        }}
        .heart-seal::before {{ left: -15px; }}
        .heart-seal::after {{ top: -15px; }}

        .controls {{ margin-top: 30px; z-index: 10; position: relative; }}
    </style>
</head>
<body>
    
    <div class="greeting" id="greetingText">For you agapi mou!<3</div>

    <div class="envelope-wrapper">
        <div class="envelope" onclick="openEnvelope()">
            <div class="flap" id="flap"><div class="heart-seal"></div></div>
            
            <!-- NEW LETTER CONTAINER FOR CLIPPING (letter is now visually 'inside') -->
            <div class="letter-container">
                <!-- Letter peek content: Se agapooo! (Now slides up from inside) -->
                <div class="letter-preview" id="letterPreview">
                     <div class="peek-message" style="color: #d6336c; font-size: 1.5rem; font-family: 'Pacifico', cursive;">Se agapooo!</div>
                </div>
            </div>

            <div class="pocket-sides"></div>
            <div class="pocket"></div>
        </div>
    </div>

    <!-- THE REAL LETTER (Full Screen Overlay) --><div class="fullscreen-letter" id="fullLetter">
        <div class="paper">
            <h2 style="color: #d6336c; font-family: 'Pacifico', cursive; margin-bottom: 0.5px;">My Dearest Nektarios... </h2>
            <p class="confession-text">
                Agapi mou, I just want to say how incredibly thankful I am to have you in my life. Who knew that one random interaction that day on the server would lead to this? Honestly, I don't regret a single second of it. Meeting you has been 
                the best thing that has ever happened to me, and I wouldn't ask for anything else. Even though we’ve only known each other for a few months, it truly feels like I’ve known you for much longer, and it doesn't change the fact 
                that I have completely fallen in love with you.
                <br><br>
                You are the most sweetest, kindest, loving, amazing, cutest, and handsome boy I have ever known. In my eyes, you are perfect. I know you have your insecurities and you sometimes don't believe you are enough or that you are handsome, but 
                please know that I love you entirely, flaws and all. What you think of yourself doesn't matter as much as this truth: I love you for who you are. You are my baby, and I promise to always give you all the love, support, and affirmation 
                that you deserve. I love you, baby. You are my world.
                <br><br>
                It's actually kind of funny that we don't have a proper anniversary yet, isn't it? Because we never really OFFICIALLY dated since neither of us ever formally asked—which I totally understand, especially since you’ve never dated before. 
                But from that very first random interaction in the server until today, you have been the absolute best part of my life, the constant light in my day. And that is why, my love, I’m finally asking you this
            </p>
            
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <a href="/proposal" class="btn btn-primary">Click Here Moroooo <3 !</a>
                <button onclick="closeFullLetter()" class="btn btn-secondary" style="font-size: 0.8rem; padding: 10px 30px;">Close Letter</button>
            </div>
        </div>
    </div>

    <!-- CONTROL BUTTONS BELOW ENVELOPE (Stateful) --><div class="controls">
        <button onclick="openEnvelope()" id="openBtn" class="btn btn-primary">Open Envelope</button>
        <button onclick="closeEnvelope()" id="closeBtn" class="btn btn-secondary" style="display: none;">Close Envelope</button>
        <button onclick="viewFullLetter(event)" id="viewFullBtn" class="btn btn-primary" style="font-size: 1.1rem; padding: 10px 20px; display: none;">View Full Letter?</button>
    </div>

    <script>
        // Heart generator specifically for when the letter is peaked
        let heartInterval;
        
        function createPeekHeart() {{
            const heartContainer = document.createElement('div');
            heartContainer.classList.add('floating-asset');
            heartContainer.classList.add('peek-heart-asset'); // Added high Z-index class
            
            const heartShape = document.createElement('div');
            heartShape.classList.add('css-heart');
            heartContainer.appendChild(heartShape);
            
            // Position hearts starting from the envelope area
            const envelope = document.querySelector('.envelope');
            const rect = envelope.getBoundingClientRect();

            heartContainer.style.left = (rect.left + 15 + (Math.random() * (rect.width - 30))) + 'px';
            heartContainer.style.bottom = (window.innerHeight - rect.bottom + 50) + 'px';
            heartContainer.style.animationDuration = (Math.random() * 4 + 3) + 's'; 
            heartContainer.style.animationDelay = '0s'; 
            // Ensures small red/pink hearts for the burst effect
            heartContainer.style.color = ['#ff0000', '#ff4d6d'][Math.floor(Math.random() * 2)]; 
            heartShape.style.transform = `scale(${{(Math.random() * 0.4 + 0.3).toFixed(2)}}) rotate(-45deg)`; // Smaller hearts for burst

            document.body.appendChild(heartContainer);

            setTimeout(() => heartContainer.remove(), 7000); 
        }}

        function updateControls(state) {{
            const openBtn = document.getElementById('openBtn');
            const viewFullBtn = document.getElementById('viewFullBtn');
            const closeBtn = document.getElementById('closeBtn');

            if (state === 'initial') {{
                openBtn.style.display = 'inline-block';
                viewFullBtn.style.display = 'none';
                closeBtn.style.display = 'none';
            }} else if (state === 'open') {{
                openBtn.style.display = 'none';
                // View Full Letter button appears below the envelope
                viewFullBtn.style.display = 'inline-block'; 
                closeBtn.style.display = 'inline-block';
            }}
        }}

       function openEnvelope() {{
            const flap = document.getElementById('flap');
            const letterPreview = document.getElementById('letterPreview');
            const envelope = document.querySelector('.envelope');
            const greeting = document.getElementById('greetingText'); // Get the greeting element

            envelope.style.animation = 'none'; // Stop wiggle
            flap.classList.add('open');
            greeting.classList.add('open'); // ADDED: Move the greeting up

            // 1. Show the letter peek
            setTimeout(() => {{
                letterPreview.classList.add('slide-up');
                // 2. Start the heart burst from the envelope (now in front!)
                heartInterval = setInterval(createPeekHeart, 100);
                // Stop the burst after a few seconds
                setTimeout(() => clearInterval(heartInterval), 2000);
                
                updateControls('open');
            }}, 200);
        }}
        
        function viewFullLetter(event) {{
            event.stopPropagation();
            const fullLetter = document.getElementById('fullLetter');
            fullLetter.classList.add('visible');
        }}

        function closeFullLetter() {{
            const fullLetter = document.getElementById('fullLetter');
            fullLetter.classList.remove('visible');
        }}

        function closeEnvelope() {{
            const flap = document.getElementById('flap');
            const letterPreview = document.getElementById('letterPreview');
            const fullLetter = document.getElementById('fullLetter');
            const envelope = document.querySelector('.envelope');
            const greeting = document.getElementById('greetingText'); // Get the greeting element

            // Clear any lingering heart interval
            clearInterval(heartInterval);
            
            closeFullLetter(); // Ensure the full screen letter is hidden
            
            setTimeout(() => {{
                letterPreview.classList.remove('slide-up');
                flap.classList.remove('open');
                greeting.classList.remove('open'); // ADDED: Move the greeting back down
                envelope.style.animation = ''; // Resume wiggle
                updateControls('initial');
            }}, 500);
        }}

        // Global floating hearts (start immediately)
        document.addEventListener('DOMContentLoaded', () => {{
            const globalHeartInterval = setInterval(createFloatingHeart, 200);
            updateControls('initial'); // Initialize buttons state
        }});

        {generator_script}
    </script>
</body>
</html>
"""

# ------------------------------------------------------------------
# PAGE 2: THE PROPOSAL (FINAL FIXED VERSION - Absolute Centering)
# ------------------------------------------------------------------
PAGE_PROPOSAL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Question?</title>
    {common_style}
    <style>
        .container {{height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;}}

        .buttons-wrapper {{ 
            margin-top: 30px; 
            display: flex; 
            gap: 20px;
            position: relative; 
            width: auto; /* <--- FIX: Allow width to shrink to content size */
            justify-content: center; 
            transition: justify-content 0.5s ease-in-out, gap 0.5s ease-in-out; 
        }}
        
        /* Base Large Size for both buttons */
        .btn-large {{
            padding: 15px 35px;
            font-size: 1.5rem;
            z-index: 2;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            min-width: 150px;
            text-align: center;
        }}
        
        /* Dynamic size classes for the NO button (shrinking) */
        #noBtn.size-1 {{ transform: scale(0.9); font-size: 1.4rem; padding: 13px 30px; }}
        #noBtn.size-2 {{ transform: scale(0.8); font-size: 1.3rem; padding: 11px 25px; }}
        #noBtn.size-3 {{ transform: scale(0.7); font-size: 1.2rem; padding: 9px 20px; }}
        #noBtn.size-4 {{ transform: scale(0.6); font-size: 1.1rem; padding: 7px 15px; }}
        #noBtn.size-5 {{ transform: scale(0.5); font-size: 1.0rem; padding: 5px 10px; }}
        #noBtn.size-6 {{ opacity: 0; pointer-events: none; transform: scale(0); margin: 0; padding: 0;}}
        
        /* Dynamic size classes for the YES button (growing) */
        #yesBtn.grow-1 {{ transform: scale(1.05); font-size: 1.6rem; padding: 16px 38px; }}
        #yesBtn.grow-2 {{ transform: scale(1.1); font-size: 1.7rem; padding: 17px 41px; }}
        #yesBtn.grow-3 {{ transform: scale(1.2); font-size: 1.8rem; padding: 18px 44px; }}
        #yesBtn.grow-4 {{ transform: scale(1.3); font-size: 1.9rem; padding: 19px 47px; }}
        #yesBtn.grow-5 {{ transform: scale(1.4); font-size: 2.0rem; padding: 20px 50px; }}
        #yesBtn.grow-6 {{ 
            transform: scale(1.6);
            font-size: 2.2rem; 
            padding: 25px 60px;
            box-shadow: 0 10px 40px rgba(255, 77, 109, 0.8);
        }}
        
        /* Adjust wrapper for centering when No is gone */
        .buttons-wrapper.centered {{
            justify-content: center;
            gap: 0;
            /* Margin auto is no longer needed since wrapper width is auto */
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 id="proposalHeader">Will you OFFICIALLY be my boyfriend?</h1>
        <div class="buttons-wrapper"> 
            <a href="/yay" id="yesBtn" class="btn btn-primary btn-large">Yes</a>
            <button id="noBtn" class="btn btn-secondary btn-large">No</button>
        </div>
    </div>

    <script>
        // Start global hearts
        document.addEventListener('DOMContentLoaded', () => {{
            {generator_script}
        }});

        (function() {{
            const yesBtn = document.getElementById('yesBtn');
            const noBtn = document.getElementById('noBtn');
            const wrapper = document.querySelector('.buttons-wrapper');
            const header = document.getElementById('proposalHeader');
            
            if (!yesBtn || !noBtn) return;

            const maxClicks = 6;
            let clickCount = 0;
            const originalNoText = noBtn.textContent;
            
            const noTexts = [
                "Are you sure?", 
                "Think again!", 
                "Come on...", 
                "Just click 'Yes'!", 
                "You know you want to!", 
                "There's only one choice!"
            ];

            function handleClick(e) {{
                e.preventDefault();
                
                if (clickCount >= maxClicks) {{
                    return; 
                }}

                // Remove previous size classes for both
                noBtn.classList.remove(`size-${{clickCount}}`); 
                yesBtn.classList.remove(`grow-${{clickCount}}`);

                // Increment click count
                clickCount++;

                // Apply new size/grow classes
                noBtn.classList.add(`size-${{clickCount}}`);
                yesBtn.classList.add(`grow-${{clickCount}}`);
                
                // Change No button text (if not fully hidden yet)
                if (clickCount < maxClicks) {{ 
                    noBtn.textContent = noTexts[clickCount - 1];
                }} else {{
                    // Final click: Hide No button and center Yes button
                    noBtn.textContent = originalNoText;
                    
                    setTimeout(() => {{ 
                        wrapper.classList.add('centered');
                    }}, 300);
                }}
            }}

            // Ensure no size/grow classes are accidentally set on page load
            for (let i = 1; i <= maxClicks; i++) {{
                yesBtn.classList.remove(`grow-${{i}}`);
                noBtn.classList.remove(`size-${{i}}`);
            }}

            noBtn.addEventListener('click', handleClick);

        }})();
    </script>
</body>
</html>
"""

# ------------------------------------------------------------------
# PAGE 3: YAY
# ------------------------------------------------------------------
PAGE_YAY = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>YAY! IT'S OFFICIAL!</title>
    <link href="https://fonts.googleapis.com/css2?family=Sacramento&display=swap" rel="stylesheet">
    {common_style}
    <style>
        /* Base page styling */
        body {{
            background-color: #ffe7ee; /* Soft Light Pink */
            background-image: radial-gradient(#ffc2d1 10%, transparent 10%), radial-gradient(#ffc2d1 10%, transparent 10%);
            background-size: 20px 20px;
            background-position: 0 0, 10px 10px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            text-align: center;
            margin: 0;
            overflow: hidden; 
        }}
        
        /* Main Text Styling (Cuter & Bolder) */
        #yayText {{
            font-family: 'Sacramento', cursive;
            font-size: 6rem;
            font-weight: 700; /* Bolder weight for the script font */
            color: #d6336c; /* Deep romantic pink */
            margin: 0;
            padding: 20px;
            animation: pulseGlow 2s infinite alternate; 
            text-shadow: 0 0 8px #fff; /* Increased base shadow */
        }}

        /* Subtext Styling (Bolder and clearer) */
        #subText {{
            font-family: 'Arial', sans-serif;
            font-size: 1.8rem;
            font-weight: bold; /* Make the subtext bold */
            color: #a4133c; 
            max-width: 80%;
            padding: 10px;
            line-height: 1.5;
            letter-spacing: 0.5px; /* Slight increase for readability */
        }}

        /* Glow Animation (More prominent glow) */
        @keyframes pulseGlow {{
            from {{
                text-shadow: 0 0 15px #ffc2d1, 0 0 30px rgba(255, 77, 109, 0.7);
            }}
            to {{
                text-shadow: 0 0 25px #ffffff, 0 0 40px #ffc2d1;
            }}
        }}

        /* Confetti and Emojis are kept */
        .confetti {{ position: absolute; width: 10px; height: 10px; animation: fall linear forwards; }}
        @keyframes fall {{ to {{ transform: translateY(100vh) rotate(720deg); }} }}
    </style>
</head>
<body>
    <h1 id="yayText">YAYYYYY!!!</h1>
    
    <p id="subText">My babyyy said yess!! I can officially call him mine now, I'm so lucky moro!! ⸜(｡˃ ᵕ ˂ )⸝♡</p>

    <script>
        function createConfetti() {{
            const c = document.createElement('div');
            c.classList.add('confetti');
            c.style.left = Math.random() * 100 + 'vw';
            // Use softer pinks/reds for the confetti
            c.style.background = ['#ffc2d1', '#ff006e', '#f77fbe', '#fff'].at(Math.floor(Math.random()*4));
            c.style.animationDuration = (Math.random()*3+2)+'s';
            document.body.appendChild(c);
            setTimeout(()=>c.remove(),5000);
        }}
        // Increase the confetti intensity slightly
        setInterval(createConfetti, 80); 
        
        document.addEventListener('DOMContentLoaded', () => {{
            {generator_script}
        }});
    </script>
</body>
</html>
"""

# ------------------------------------------------------------------
# ROUTES 
# ------------------------------------------------------------------

@app.route('/')
def home(): 
    return render_template_string(PAGE_ENVELOPE.format(
        common_style=COMMON_STYLE, 
        generator_script=GENERATOR_SCRIPT
    ))

@app.route('/proposal')
def proposal(): 
    return render_template_string(PAGE_PROPOSAL.format(
        common_style=COMMON_STYLE, 
        generator_script=GENERATOR_SCRIPT
    ))

@app.route('/yay')
def yay(): 
    return render_template_string(PAGE_YAY.format(
        common_style=COMMON_STYLE, 
        generator_script=GENERATOR_SCRIPT
    ))

if __name__ == '__main__':


