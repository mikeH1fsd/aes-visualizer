/* =====================================================
   GLOBAL STATE
===================================================== */

let currentOperation = "1"; // 1 encrypt | 2 decrypt
let currentFormat = "1";    // 1 text | 2 hex | 3 base64
let currentKeySize = "1";   // 1 128 | 2 192 | 3 256
let currentMode = "1";      // 1 ECB | 2 CBC

let latestResponse = null;

/* =====================================================
   DOM LOADED
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    setupToggleButtons();

    setupTabs();

    setupActions();
    
    setupKeyExpansion();

});

/* =====================================================
   TOGGLE BUTTONS
===================================================== */

function setupToggleButtons(){

    /* OPERATION */

    document.querySelectorAll("[data-operation]").forEach(btn => {

        btn.addEventListener("click", () => {

            setActiveButton("[data-operation]", btn);

            currentOperation = btn.dataset.operation;

            updateDataLabel();
        });
    });

    /* DATA FORMAT */

    document.querySelectorAll("[data-format]").forEach(btn => {

        btn.addEventListener("click", () => {

            setActiveButton("[data-format]", btn);

            currentFormat = btn.dataset.format;
        });
    });

    /* KEY SIZE */

    document.querySelectorAll("[data-keysize]").forEach(btn => {

        btn.addEventListener("click", () => {

            setActiveButton("[data-keysize]", btn);

            currentKeySize = btn.dataset.keysize;
        });
    });

    /* MODE */

    document.querySelectorAll("[data-mode]").forEach(btn => {

        btn.addEventListener("click", () => {

            setActiveButton("[data-mode]", btn);

            currentMode = btn.dataset.mode;

            toggleIV();
        });
    });

}

/* =====================================================
   ACTIVE BUTTON
===================================================== */

function setActiveButton(selector, activeBtn){

    document.querySelectorAll(selector).forEach(btn => {

        btn.classList.remove("active");

    });

    activeBtn.classList.add("active");
}

/* =====================================================
   UPDATE LABEL
===================================================== */

function updateDataLabel(){

    const label = document.getElementById("dataLabel");

    if(currentOperation === "1"){

        label.innerText = "Plaintext";

    }else{

        label.innerText = "Ciphertext";
    }
}

/* =====================================================
   TOGGLE IV
===================================================== */

function toggleIV(){

    const ivContainer = document.getElementById("ivContainer");

    if(currentMode === "2"){

        ivContainer.style.display = "block";

    }else{

        ivContainer.style.display = "none";
    }
}

/* =====================================================
   ACTION BUTTONS
===================================================== */

function setupActions(){

    document.getElementById("processBtn")
        .addEventListener("click", processAES);

    document.getElementById("clearBtn")
        .addEventListener("click", clearAll);
}

/* =====================================================
   PROCESS AES
===================================================== */

async function processAES(){

    const dataInput = document.getElementById("dataInput").value;

	let secretKey =
	    document.getElementById("secretKey").value;

	/* AUTO GENERATE IF EMPTY */

	if(secretKey.trim() === ""){

	    generateRandomKey();

	    secretKey =
		document.getElementById("secretKey").value;
	}

    const ivInput = document.getElementById("ivInput").value;

    /* VALIDATION */

    const requiredKeyLength = getRequiredKeyLength();

    if(secretKey.length !== requiredKeyLength){

        alert(
            `Invalid key length.\n` +
            `AES requires ${requiredKeyLength} bytes.`
        );

        return;
    }

    /* BUILD JSON PAYLOAD */

    const payload = {

        operation: currentOperation,

        data: dataInput,

        data_format: currentFormat,

        key: secretKey,

        key_choice: currentKeySize,

        mode: currentMode,

        iv: ivInput
    };

    console.log(payload);

    try{

        const response = await fetch("/api/process", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)
        });

        const result = await response.json();

        console.log(result);

        latestResponse = result;

        renderOutput(result);

        renderRoundView(result);

        renderBlockView(result);

    }catch(error){

        console.error(error);

        alert("Server Error");
    }
}

/* =====================================================
   KEY LENGTH
===================================================== */

function getRequiredKeyLength(){

    if(currentKeySize === "1") return 16;

    if(currentKeySize === "2") return 24;

    return 32;
}

/* =====================================================
   OUTPUT
===================================================== */

function renderOutput(result){

    /* STATUS */

    document.getElementById("resultStatus").value =
        result.status || "";

    /* AES MODE */

    document.getElementById("resultMode").value =
        result.aes_mode || "";

    /* HEX */

    document.getElementById("resultHex").value =
        result.result_hex || "";

    /* BASE64 */

    document.getElementById("resultBase64").value =
        result.result_base64 || "";

    /* ASCII */

    document.getElementById("resultAscii").value =
        result.result_ascii || "";

    /* ERROR */

    if(result.status === "error"){

        alert(result.message || "Unknown Error");
    }
}

/* =====================================================
   ROUND VIEW
===================================================== */

function renderRoundView(result){

    if(!result.logs) return;

    const blockSelect =
        document.getElementById("blockSelect");

    const roundSelect =
        document.getElementById("roundSelect");

    /* CLEAR */

    blockSelect.innerHTML = "";

    roundSelect.innerHTML = "";

    /* LOAD BLOCKS */

    result.logs.forEach((block, index) => {

        const option = document.createElement("option");

        option.value = index;

        option.textContent = `Block ${block.block}`;

        blockSelect.appendChild(option);
    });

    /* FIRST LOAD */

    loadRounds(0);

    renderSingleRound(0, 0);

    /* BLOCK CHANGE */

    blockSelect.onchange = () => {

        const blockIndex =
            parseInt(blockSelect.value);

        loadRounds(blockIndex);

        renderSingleRound(blockIndex, 0);
    };

    /* ROUND CHANGE */

    roundSelect.onchange = () => {

        const blockIndex =
            parseInt(blockSelect.value);

        const roundIndex =
            parseInt(roundSelect.value);

        renderSingleRound(
            blockIndex,
            roundIndex
        );
    };
}

/* =====================================================
   BLOCK VIEW
===================================================== */

function renderBlockView(result){

    const container =
        document.getElementById("blockContainer");

    container.innerHTML = "";

    if(!result.logs) return;

    result.logs.forEach(block => {

        const card = document.createElement("div");

        card.className = "block-card";

        let html = `
            <div class="block-title">
                Block ${block.block}
            </div>
        `;

        html += `
            <div class="block-line">
                <strong>Initial:</strong>
                ${block.initial_block_data}
            </div>
        `;

        if(block.cbc_mode_info){

            Object.keys(block.cbc_mode_info)
                .forEach(key => {

                html += `
                    <div class="block-line">

                        <strong>${key}:</strong>

                        ${block.cbc_mode_info[key]}

                    </div>
                `;
            });
        }

        card.innerHTML = html;

        container.appendChild(card);
    });
}

/* =====================================================
   MATRIX RENDER
===================================================== */
function renderMatrix(hexString){

    if(!hexString){

        return "";
    }

    /*
        Convert:
        AABBCCDDEEFF...
        ->
        ["AA","BB","CC"...]
    */

    const bytes =
        hexString.match(/.{1,2}/g) || [];

    /*
        AES STATE
        COLUMN-MAJOR

        [ 0  4  8 12 ]
        [ 1  5  9 13 ]
        [ 2  6 10 14 ]
        [ 3  7 11 15 ]
    */

    let html = `
        <table class="aes-matrix">
    `;

    for(let row = 0; row < 4; row++){

        html += "<tr>";

        for(let col = 0; col < 4; col++){

            const index =
                col * 4 + row;

            html += `
                <td>
                    ${bytes[index] || "00"}
                </td>
            `;
        }

        html += "</tr>";
    }

    html += "</table>";

    return html;
}

/* =====================================================
   SPLIT HEX
===================================================== */

function splitHex(hex){

    const clean = hex.replace(/\s+/g, "");

    const arr = [];

    for(let i=0; i<clean.length; i+=2){

        arr.push(clean.substring(i, i+2));
    }

    return arr;
}

/* =====================================================
   CLEAR
===================================================== */

function clearAll(){

    document.getElementById("dataInput").value = "";

    document.getElementById("secretKey").value = "";

    document.getElementById("ivInput").value = "";

    document.getElementById("resultHex").value = "";

    document.getElementById("resultBase64").value = "";

    document.getElementById("resultAscii").value = "";

    document.getElementById("resultStatus").value = "";

    document.getElementById("resultMode").value = "";

    document.getElementById("roundContainer").innerHTML = "";

    document.getElementById("blockContainer").innerHTML = "";
}
/* =====================================================
   TABS
===================================================== */

function setupTabs(){

    document.querySelectorAll(".tab-btn")
        .forEach(btn => {

        btn.addEventListener("click", () => {

            document.querySelectorAll(".tab-btn")
                .forEach(b => {

                b.classList.remove("active");
            });

            btn.classList.add("active");

            const tabId = btn.dataset.tab;

            document.querySelectorAll(".tab-content")
                .forEach(tab => {

                tab.classList.remove("active");
            });

            document.getElementById(tabId)
                .classList.add("active");
        });
    });
}


function loadRounds(blockIndex){

    const roundSelect =
        document.getElementById("roundSelect");

    roundSelect.innerHTML = "";

    const rounds =
        latestResponse.logs[blockIndex].rounds;

    rounds.forEach((round, index) => {

        const option =
            document.createElement("option");

        option.value = index;

        option.textContent =
            `Round ${round.round}`;

        roundSelect.appendChild(option);
    });
}

function renderSingleRound(
    blockIndex,
    roundIndex
){

    const container =
        document.getElementById("roundContainer");

    container.innerHTML = "";

    const round =
        latestResponse.logs[blockIndex]
        .rounds[roundIndex];

    let html = `
        <div class="round-card">

            <div class="round-title">
                Block ${blockIndex}
                -
                Round ${round.round}
            </div>
    `;

    const orderedSteps = [

    "SubBytes",
    "ShiftRows",
    "MixColumns",
    "AddRoundKey",

    "InvSubBytes",
    "InvShiftRows",
    "InvMixColumns",
    "AddRoundKey_Inv"
    ];
    
    
/* RENDER THEO THỨ TỰ AES */

orderedSteps.forEach(step => {

    if(round[step]){

        html += `
            <div class="matrix-wrapper">

                <h3>${step}</h3>

                ${renderMatrix(round[step])}

            </div>
        `;
    }
});  

    
    html += `</div>`;

    container.innerHTML = html;
}

/* =========================================
   RANDOM AES KEY
========================================= */
/* =========================================
   RANDOM AES KEY
========================================= */

/* =========================================
   RANDOM AES KEY
========================================= */

document
    .getElementById("generateKeyBtn")
    .addEventListener("click", generateRandomKey);

function generateRandomKey(){

    let length = 16;

    /*
        AES-128 => 16 bytes
        AES-192 => 24 bytes
        AES-256 => 32 bytes
    */

    if(currentKeySize === "2"){

        length = 24;
    }

    else if(currentKeySize === "3"){

        length = 32;
    }

    const chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    let key = "";

    for(let i = 0; i < length; i++){

        key += chars.charAt(
            Math.floor(Math.random() * chars.length)
        );
    }

    document.getElementById("secretKey").value = key;
}


/* =====================================================
   KEY EXPANSION
===================================================== */

function setupKeyExpansion(){

    document
        .getElementById("loadKeyExpansionBtn")
        .addEventListener(
            "click",
            loadKeyExpansion
        );
}


async function loadKeyExpansion(){

    const secretKey =
        document.getElementById("secretKey").value;

    if(secretKey.trim() === ""){

        alert("Please enter key first");

        return;
    }

    const payload = {

        key: secretKey,

        key_choice: currentKeySize
    };

    try{

        const response = await fetch(
            "/api/key-expansion",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(payload)
            }
        );

        const result =
            await response.json();

        console.log(result);

        renderKeyExpansion(result);

    }catch(error){

        console.error(error);

        alert("Key Expansion Error");
    }
}

function renderKeyExpansion(result){

    const container =
        document.getElementById(
            "keyExpansionContainer"
        );

    container.innerHTML = "";

    if(result.status !== "success"){

        container.innerHTML =
            `<div class="error-box">
                ${result.message}
            </div>`;

        return;
    }

    result.key_schedule.forEach(roundKey => {

        const card =
            document.createElement("div");

        card.className =
            "round-card";

        card.innerHTML = `

            <div class="round-title">

                Round ${roundKey.round}

            </div>

            <div class="matrix-wrapper">

                ${renderMatrix(
                    roundKey.key_hex
                )}

            </div>
        `;

        container.appendChild(card);
    });
}

