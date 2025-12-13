(function () {
    'use strict';

    // -----------------------------
    // IMPORTED CONFIG FROM HTML
    // -----------------------------
    const configScript = document.getElementById('price-config');
    const CONFIG = {
        currency: configScript.dataset.currency,
        decimalsEnabled: configScript.dataset.showDecimals == "True" ? true : false,
        decimalPlaces: parseInt(configScript.dataset.decimalPlaces)
    };
	
    // -----------------------------
    // DOM REFERENCES
    // -----------------------------
    const elements = {
        oldPrice: document.getElementById('oldprice'),
        newPrice: document.getElementById('newprice'),
        printQty: document.getElementById('printqty'),
        salepart: document.getElementById('salepart'),
        form: document.querySelector('form'),
        reprintBtn: document.getElementById('reprint'),
        priceButtons: document.getElementById('price-buttons'),
        qtyButtons: document.querySelectorAll('.qpc[data-qty]'),
        oldNewRadios: document.querySelectorAll('input[name="oldnew"]'),
        newPriceStar: document.getElementById('newprice-star'),
        cleanupBtn: document.getElementById('cleanup'),
        clearhistoryBtn: document.getElementById('clearhistory'),
        prevPrints: document.getElementById('prevprints'),
        timeSavedLabel: document.getElementById('time_saved')
    };

    // -----------------------------
    // CONSTANTS
    // -----------------------------
    const STORAGE_KEYS = {
        PRICE_HISTORY: 'priceHistory',
        SELECTED_PRICE_TYPE: 'selectedPriceType'
    };

    const MAX_HISTORY = 3;

    // -----------------------------
    // UTILITY FUNCTIONS
    // -----------------------------
    function safeLocalStorage(op, key, value) {
        try {
            if (op === 'get') return localStorage.getItem(key);
            if (op === 'set') return localStorage.setItem(key, value);
        } catch (err) {
            console.warn('LocalStorage Error:', err);
            return null;
        }
    }

    const getSelectedRadio = name =>
        document.querySelector(`input[name="${name}"]:checked`);

    function updateSaleVisibility(type) {
        const isSale = type === 'old';
        elements.salepart.style.display = isSale ? 'block' : 'none';
        elements.newPriceStar.style.display = isSale ? 'none' : 'inline-block';
    }

    function appendPrintQtyToLocalStorage() {
        try {
            // Get current quantity from localStorage if exists
            let qty = safeLocalStorage('get', 'lastPrintQty');;
            qty = qty ? parseInt(qty) : 0;

            // Increment quantity
            qty += parseInt(elements.printQty.value) || 0;
            safeLocalStorage('set', 'lastPrintQty', qty.toString());
        } catch (err) {
            console.warn('LocalStorage Error:', err);
        }
    }

    function updateTimeSavedLabel() {
        try {
            let qty = safeLocalStorage('get', 'lastPrintQty');
            qty = qty ? parseInt(qty) : 0;
            const timeSavedSeconds = qty * 45; // 45 seconds per label 


            // if more than 1 day, show days too
            if (timeSavedSeconds >= 86400) {
                const days = Math.floor(timeSavedSeconds / 86400);
                const hours = Math.floor((timeSavedSeconds % 86400) / 3600);
                const minutes = Math.floor((timeSavedSeconds % 3600) / 60);
                const seconds = Math.round(timeSavedSeconds % 60);
                let displayText = '';
                displayText += `${days} d `;
                if (hours > 0) displayText += `${hours} hr `;
                if (minutes > 0) displayText += `${minutes} min `;
                displayText += `${seconds} sec`;
                elements.timeSavedLabel.textContent = displayText;
                return;
            }

            // if more than 1 hour, show hours too
            if (timeSavedSeconds >= 3600) {
                const hours = Math.floor(timeSavedSeconds / 3600);
                const minutes = Math.floor((timeSavedSeconds % 3600) / 60);
                const seconds = Math.round(timeSavedSeconds % 60);
                let displayText = '';
                displayText += `${hours} hr `;
                if (minutes > 0) displayText += `${minutes} min `;
                displayText += `${seconds} sec`;
                elements.timeSavedLabel.textContent = displayText;
                return;
            }

            const minutes = Math.floor(timeSavedSeconds / 60);
            const seconds = Math.round(timeSavedSeconds % 60);
            let displayText = '';
            if (minutes > 0) displayText += `${minutes} min `;
            displayText += `${seconds} sec`;
            elements.timeSavedLabel.textContent = displayText;
        } catch (err) {
            console.warn('LocalStorage Error:', err);
        }
    }

    // -----------------------------
    // EVENT HANDLERS
    // -----------------------------
    function handlePriceClick(e) {
        const btn = e.target.closest('.price');
        if (!btn) return;

        const price = btn.dataset.price;
        const mode = getSelectedRadio('oldnew')?.value;
        if (!mode) return;

        (mode === 'old' ? elements.oldPrice : elements.newPrice).value = price;
    }

    function handleQtyClick(e) {
        const qty = e.target.dataset.qty;
        if (qty) elements.printQty.value = qty;
    }

    function handlePriceMode(e) {
        const type = e.target.value;
        safeLocalStorage('set', STORAGE_KEYS.SELECTED_PRICE_TYPE, type);
        cleanup();
        updateSaleVisibility(type);
    }

    function handleSubmit(e) {
        e.preventDefault();

        const oldP = elements.oldPrice.value;
        let newP = elements.newPrice.value;
        const discountRadio = getSelectedRadio('discount');
        let discountID = discountRadio ? discountRadio.id : '0';

        // Validation logic preserved
        if (!oldP && !newP && discountID === '0') return;
        if (oldP && !newP && discountID === '0') return;
        if (discountID !== '0' && !oldP) return;

        if (oldP && isNaN(oldP)) return;
        if (newP && isNaN(newP)) return;

        if (oldP == "-0") return;
        if (newP == "-0") return;

        // Auto-calc discount when user enters both prices
        if (oldP && newP && discountID === '0') {
            discountID = Math.round((100 - (newP / oldP) * 100).toFixed(2));
            document.getElementById("0").value = newP / oldP;
        }

        const entry = { old: oldP, new: newP, discount: discountID };
        updateHistory(entry);

        appendPrintQtyToLocalStorage();
        updateTimeSavedLabel();

        setTimeout(() => e.target.submit(), 50);
    }

    function handleReprint() {
        const history = JSON.parse(
            safeLocalStorage('get', STORAGE_KEYS.PRICE_HISTORY) || '[]'
        );

        if (!history.length) return alert("No recent print data found.");

        fillForm(history[0]);
        elements.printQty.value = 1;
        
        const oldP = elements.oldPrice.value;
        let newP = elements.newPrice.value;
        const discountRadio = getSelectedRadio('discount');
        let discountID = discountRadio ? discountRadio.id : '0';

        // Validation logic preserved
        if (!oldP && !newP && discountID === '0') return;
        if (oldP && !newP && discountID === '0') return;
        if (discountID !== '0' && !oldP) return;

        // Auto-calc discount when user enters both prices
        if (oldP && newP && discountID === '0') {
            discountID = Math.round((100 - (newP / oldP) * 100).toFixed(2));
            document.getElementById("0").value = newP / oldP;
        }

        appendPrintQtyToLocalStorage();
        updateTimeSavedLabel();

        elements.form.submit();
    }

    function cleanup() {
        elements.oldPrice.value = '';
        elements.newPrice.value = '';
        elements.printQty.value = '';
        document.getElementById("0").checked = true;
    }

    function clearHistory() {
        safeLocalStorage('set', STORAGE_KEYS.PRICE_HISTORY, JSON.stringify([]));
        const recentContainer = document.getElementById('recentContainer');
        if (recentContainer) recentContainer.remove();
        renderHistory();
    }

    // -----------------------------
    // HISTORY SYSTEM
    // -----------------------------
    function updateHistory(entry) {
        let list = JSON.parse(
            safeLocalStorage('get', STORAGE_KEYS.PRICE_HISTORY) || '[]'
        );

        const exists = list.some(x =>
            x.old === entry.old &&
            x.new === entry.new &&
            x.discount === entry.discount
        );

        if (!exists) {
            list.unshift(entry);
            list = list.slice(0, MAX_HISTORY);
            safeLocalStorage('set', STORAGE_KEYS.PRICE_HISTORY, JSON.stringify(list));
        }
    }

    function fillForm(entry) {
        if (entry.old) elements.oldPrice.value = entry.old;
        if (entry.new) elements.newPrice.value = entry.new;

        const radio = document.getElementById(entry.discount);
        if (radio) radio.checked = true;
    }

    function createHistoryButton(entry) {
        const btn = document.createElement('button');
        btn.className = 'recent-label col-4';
        btn.type = 'button';

        let newPriceFormatted;
        let oldFormatted;

        if (entry.old && entry.discount !== '0') {
            const calculated =
                entry.new ||
                (entry.old * (1 - entry.discount / 100));

            newPriceFormatted = CONFIG.decimalsEnabled
                ? Number(calculated).toFixed(CONFIG.decimalPlaces)
                : Math.round(calculated);

            oldFormatted = CONFIG.decimalsEnabled
                ? Number(entry.old).toFixed(CONFIG.decimalPlaces)
                : entry.old;

            btn.innerHTML = `
                <div class="sale-label-style mx-1">
                    <span class="label-text text-decoration-line-through text-nowrap"> ${oldFormatted} ${CONFIG.currency} </span><br>
                    <span class="label-text text-nowrap">- ${entry.discount}%</span><br>
                    <span class="label-text text-nowrap">${newPriceFormatted} ${CONFIG.currency}</span>
                </div>`;
        } else {
            newPriceFormatted = CONFIG.decimalsEnabled
                ? Number(entry.new).toFixed(CONFIG.decimalPlaces)
                : entry.new;

            btn.innerHTML = `
                <div class="normal-label-style mx-1">
                    <span class="label-text text-nowrap">${newPriceFormatted} ${CONFIG.currency}</span>
                </div>`;
        }

        btn.addEventListener('click', () => fillForm(entry));
        return btn;
    }

    function renderHistory() {
        const history = JSON.parse(
            safeLocalStorage('get', STORAGE_KEYS.PRICE_HISTORY) || '[]'
        );

        const row = document.createElement('div');
        row.id = "recentGrid";
        row.className = "row";

        if (!history.length) {
            row.textContent = "History will show here...";
            row.style.color = "white";
            row.style.marginLeft = "0px";
        } else {
            history.forEach(entry => row.appendChild(createHistoryButton(entry)));
        }

        const wrapper = document.createElement('div');
        wrapper.id = "recentContainer";
        wrapper.appendChild(row);

        elements.form.insertBefore(wrapper, elements.prevPrints);
    }

    // -----------------------------
    // INITIALIZATION
    // -----------------------------
    function loadSavedMode() {
        const saved = safeLocalStorage('get', STORAGE_KEYS.SELECTED_PRICE_TYPE);
        const type = saved || 'old';

        const radio = document.querySelector(`input[name="oldnew"][value="${type}"]`);
        if (radio) radio.checked = true;

        if (!saved) safeLocalStorage('set', STORAGE_KEYS.SELECTED_PRICE_TYPE, type);

        updateSaleVisibility(type);
    }

    function addListeners() {
        elements.form.addEventListener('submit', handleSubmit);
        elements.reprintBtn.addEventListener('click', handleReprint);
        elements.cleanupBtn.addEventListener('click', cleanup);
        elements.clearhistoryBtn.addEventListener('click', clearHistory);
        

        elements.priceButtons.addEventListener('click', handlePriceClick);

        elements.qtyButtons.forEach(btn =>
            btn.addEventListener('click', handleQtyClick)
        );

        elements.oldNewRadios.forEach(r =>
            r.addEventListener('change', handlePriceMode)
        );
    }

    function init() {
        loadSavedMode();
        renderHistory();
        addListeners();
        updateTimeSavedLabel();
    }

    document.readyState === 'loading'
        ? document.addEventListener('DOMContentLoaded', init)
        : init();

})();
