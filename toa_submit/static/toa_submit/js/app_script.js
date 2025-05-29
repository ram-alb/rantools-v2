function add5GInput(ip) {
    let div = document.createElement('div');
    div.className = 'form-group';
    div.id = '5G-input-container';

    let label = document.createElement('label');
    label.setAttribute('for', 'tr-nr');
    label.innerText = 'TR-NR:';

    let input = document.createElement('input');
    input.type = 'text';
    input.id = 'tr-nr';
    input.name = 'tr-nr';
    input.value = ip;

    div.appendChild(label);
    div.appendChild(input);

    let formContainer = document.getElementById('add-data');
    formContainer.appendChild(div);

    // Создаем контейнер для чекбоксов
    let checkboxGroup = document.createElement('div');
    checkboxGroup.className = 'checkbox-group'; // Добавляем класс для стилизации

    // Функция для создания чекбокса и его label
    function createCheckbox(name, value, text) {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = name;
        checkbox.value = value;

        const label = document.createElement('label');
        label.textContent = text;
        label.prepend(checkbox); // Чекбокс перед текстом
        return label;
    }

    // Добавляем чекбоксы в контейнер
    checkboxGroup.appendChild(createCheckbox('5g_band', '78', '3600'));
    checkboxGroup.appendChild(createCheckbox('5g_band', '5', '700'));

    // Создаем fieldset для 5G Bands
    let fieldset5G = document.createElement('fieldset');
    fieldset5G.id = '5G-Data';

    let legend = document.createElement('legend');
    legend.textContent = '5G Bands';
    fieldset5G.appendChild(legend);
    fieldset5G.appendChild(checkboxGroup); // Вставляем чекбоксы внутрь fieldset

    let formContainerBands = document.getElementById('Bands');
    formContainerBands.style.display = 'block';
    formContainerBands.appendChild(fieldset5G);
}


function remove5GInput() {
    let container = document.getElementById('5G-input-container');
    if (container) {
        container.remove();
    }

    let containerBand = document.getElementById('5G-Data');
    if (containerBand) {
        containerBand.remove();
    }

}

function add4GInput(ip) {
    let div = document.createElement('div');
    div.className = 'form-group';
    div.id = '4G-Input-container';

    let label = document.createElement('label');
    label.setAttribute('for', 'tr-s1');
    label.innerText = 'TR-S1:';

    let input = document.createElement('input');
    input.id = 'tr-s1';
    input.name = 'tr-s1';
    input.value = ip;
    div.appendChild(label);
    div.appendChild(input)
    
    let formContainer = document.getElementById('add-data');
    formContainer.appendChild(div);

    let checkboxGroup = document.createElement('div');
    checkboxGroup.className = 'checkbox-group';

    function createCheckbox(name, value, text) {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = name;
        checkbox.value = value;

        const label = document.createElement('label');
        label.textContent = text;
        label.prepend(checkbox); // Чекбокс перед текстом
        return label;
    }



    checkboxGroup.appendChild(createCheckbox('4g_band', '5', '700'));
    checkboxGroup.appendChild(createCheckbox('4g_band', '20', '800'));
    checkboxGroup.appendChild(createCheckbox('4g_band', '3', '1800'));
    checkboxGroup.appendChild(createCheckbox('4g_band', '1', '2100'));

    // Создаем fieldset для 4G Bands
    let fieldset4G = document.createElement('fieldset');
    fieldset4G.id = '4G-Data';

    let legend = document.createElement('legend');
    legend.textContent = '4G Bands';
    fieldset4G.appendChild(legend);
    fieldset4G.appendChild(checkboxGroup); // Вставляем чекбоксы внутрь fieldset

    let formContainerBands = document.getElementById('Bands');
    formContainerBands.style.display = 'block';
    formContainerBands.appendChild(fieldset4G);
}

function remove4GInput() {
    let container = document.getElementById('4G-Input-container');
    if (container) {
        container.remove();
    }
    
    let containerBand = document.getElementById('4G-Data');
    if (containerBand) {
        containerBand.remove();
    }

}

function add3GInput(ip) {
    let div = document.createElement('div');
    div.className = 'form-group';
    div.id = '3G-Input-container';

    let label = document.createElement('label');
    label.setAttribute('for', 'tr-iub');
    label.innerText = 'TR-IUB:';

    let input = document.createElement('input');
    input.id = 'tr-iub';
    input.name = 'tr-iub';
    input.value = ip;
    div.appendChild(label);
    div.appendChild(input)

    let formContainer = document.getElementById('add-data');
    formContainer.appendChild(div);
}

function remove3GInput() {
    let container = document.getElementById('3G-Input-container');
    if (container) {
        container.remove();
    }
}

function add2GInput(ip) {
    let div = document.createElement('div');
    div.className = 'form-group';
    div.id = '2G-Input-container';

    let label = document.createElement('label');
    label.setAttribute('for', 'tr-abis');
    label.innerText = 'TR-ABIS:';

    let input = document.createElement('input');
    input.id = 'tr-abis';
    input.name = 'tr-abis';
    input.value = ip;
    div.appendChild(label);
    div.appendChild(input)

    let formContainer = document.getElementById('add-data');
    formContainer.appendChild(div);
}

function remove2GInput() {
    let container = document.getElementById('2G-Input-container');
    if (container) {
        container.remove();
    }
}


function populateCombobox(data) {
    const combobox = document.getElementById('combobox-handler')
    combobox.innerHTML = ''
    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.name + ', ' + item.mobile;
        option.textContent = item.name;
        combobox.appendChild(option);
    });    
}

function populateCabinetCombo(data) {
    console.log(data)
    const combobox = document.getElementById('combobox-dictionary')
    combobox.innerHTML = ''
    for (const [key, value] of Object.entries(data)) {
        const option = document.createElement('option');
        option.value = value;      
        option.textContent = key;  
        combobox.appendChild(option);  
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // === index.html logic ===
    const siteNameInputIndex = document.querySelector('input[name="site_name"]');
    const checkboxesIndex = document.querySelectorAll('input[name="technologies"]');
    const submitButtonIndex = document.getElementById('btn');

    if (siteNameInputIndex && checkboxesIndex.length > 0 && submitButtonIndex) {
        function toggleButtonState() {
            const siteFilled = siteNameInputIndex.value.trim() !== '';
            const anyCheckboxChecked = Array.from(checkboxesIndex).some(checkbox => checkbox.checked);
            submitButtonIndex.disabled = !(siteFilled && anyCheckboxChecked);
        }

        siteNameInputIndex.addEventListener('input', toggleButtonState);
        checkboxesIndex.forEach(checkbox => checkbox.addEventListener('change', toggleButtonState));
        toggleButtonState();
        const input = document.getElementById('input-field');
        const btn = document.getElementById('btn');

        btn.addEventListener('click', () => {
            const inputVal = input.value;
            if (inputVal.length >= 5) {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>Loading...';
            }
        });    
    }

    // === search.html logic ===
    const siteNameInputSearch = document.getElementById('sitename');
    const sendToaBtn = document.getElementById('send-toa-button');

    if (siteNameInputSearch && sendToaBtn) {
        const siteInfo = window.site_info || {};
        const commonData = window.common_data || {};
        const acceptedList = window.accepted_list || [];
        const cabinetType = window.cabinet_type || {};
        const technologies = window.technologies || [];
        const data2G = window.data_2g || null;
        const data3G = window.data_3g || null;

        displaySiteInfo(siteInfo);
        populateCabinetCombo(cabinetType);
        populateCombobox(acceptedList);
        displayAdditionalData(commonData);

        if (!technologies.includes('5G')) {
            remove5GInput();
        } else {
            add5GInput(commonData.NR);
        }

        if (!technologies.includes('4G')) {
            remove4GInput();
        } else {
            add4GInput(commonData.S1);
        }

        if ((!technologies.includes('5G') && !technologies.includes('4G'))) {
            remove4GInput();
            remove5GInput();
            const bands = document.getElementById('Bands');
            if (bands) bands.style.display = 'none';
        }

        if (!technologies.includes('2G')) {
            remove2GInput();
            const field2G = document.getElementById('2G-Data');
            if (field2G) field2G.style.display = 'none';
        } else {
            add2GInput(commonData.Abis);
            const field2G = document.getElementById('2G-Data');
            if (field2G) field2G.style.display = 'block';
            if (data2G) display2GData(data2G);
        }

        if (!technologies.includes('3G')) {
            remove3GInput();
            const field3G = document.getElementById('3G-Data');
            if (field3G) field3G.style.display = 'none';
        } else {
            add3GInput(commonData.Iub);
            const field3G = document.getElementById('3G-Data');
            if (field3G) field3G.style.display = 'block';
            if (data3G) display3GData(data3G);
        }
    }

    // Helpers for search.html
    function displaySiteInfo(data) {
        if (!data) return;
        document.getElementById('sitename').value = data.sitename || '';
        document.getElementById('latitude').value = data.latitude || '';
        document.getElementById('longitude').value = data.longitude || '';
        document.getElementById('address').value = data.address || '';
        document.getElementById('kato').value = data.kato || '';
    }

    function displayAdditionalData(data) {
        if (!data) return;
        document.getElementById('tr-oam').value = data.OAM || '';
        document.getElementById('serial-number').value = data.SN || '';
        document.getElementById('subnetwork').value = data.SubNetwork || '';
        document.getElementById('PName').value = data.PName || '';
    }

    function display2GData(data) {
        document.getElementById('2g_data_ne').value = data.NE || '';
        document.getElementById('2g_data_lac').value = data.LAC || '';
        document.getElementById('2g_data_cell_list').value = data.CID || '';
        document.getElementById('2g_data_CI_list').value = data.CLIST || '';
        document.getElementById('2g_data_tg').value = data.TG || '';
        document.getElementById('2g_data_trx').value = data.TRX || '';
        document.getElementById('2g_data_edge').value = data.EDGE || '';
    }

    function display3GData(data) {
        document.getElementById('3g_data_ne').value = data.NE || '';
        document.getElementById('3g_data_lac').value = data.LAC || '';
        document.getElementById('3g_data_cell_list').value = data.CID || '';
        document.getElementById('3g_data_CI_list').value = data.CLIST || '';
    }
});

function validateForm(){
            const container = document.getElementById('Bands');
            if (getComputedStyle(container).display !== 'none') {
                const fieldsets = container.querySelectorAll('fieldset');
                for (let fieldset of fieldsets) {
                    const checkboxes = fieldset.querySelectorAll('input[type="checkbox"]');
                    const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
                
                    if (!isChecked) {
                        alert('Please choose at least one band')
                        return false;
                    }
                }
            }
            return true;    
        };


    document.getElementById('reset-button').addEventListener('click', function(event) {
            event.preventDefault(); 
            const confirmation = confirm('Confirm close this page')
            if (confirmation){
                const form = document.getElementById('site-form')
                if (!form) {
                    console.error('Form not found');
                    return;
                };

                const formData = new FormData(form);
                
                formData.set('action', 'reset');

                fetch('/toa_submit/create/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                            'X-Requested-With': 'XMLHttpRequest',  
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data)        
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    } else {
                        console.error('No redirect URL found in response');
                    }
                }) 
                .catch(error => console.error('Error:', error));
            }
        });
    
    async function get2GSiteName(sitename) {
            try {
                const response = await fetch(`/toa_submit/api/get-site-name/?sitename=${encodeURIComponent(sitename)}`);
                if (!response.ok) {
                    console.error("Ошибка API:", await response.text());
                    return sitename;  // Возвращаем оригинальный sitename, если ошибка
                }

                const data = await response.json();
                return data.site_name || sitename;  // Если site_name нет, вернуть исходный sitename
            } catch (error) {
                console.error("Ошибка запроса:", error);
                return sitename;
            }
        };

    document.getElementById('send-toa-button').addEventListener('click', async function(event) {
        event.preventDefault();
        if (!validateForm()) {
            return;
        }

        const confirmation = confirm('Confirm send toa')
        if (!confirmation) return;

        const form = document.getElementById('site-form');
        let disabledElements = form.querySelectorAll('input:disabled');
        disabledElements.forEach(function(element) {
            element.disabled = false;
        });

        const formData = new FormData(form);
        formData.append('action', 'send_toa');

        const technologiesRaw = document.getElementById('send-toa-button').dataset.technologies;
        let technologies = technologiesRaw ? technologiesRaw.split(',') : [];
        console.log(technologiesRaw);
        
        const sitename = document.getElementById('sitename').value;
        const address = document.getElementById('address').value;
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        const KATO = document.getElementById("kato").value;
        const serialNumber = document.getElementById('serial-number').value;
        const subNetwork = document.getElementById('subnetwork').value;
        const dateValue = document.getElementById('toa-date').value;
        let toaDate;
        if (dateValue) {
            const [year, month, day] = dateValue.split('-');
            toaDate = `${day}.${month}.${year}`;
        }
        const accepted = document.getElementById('combobox-handler');
        const acceptedValue = accepted.value;
        const cabinetTypes = document.getElementById('combobox-dictionary');
        const cabinetValue = cabinetTypes.value;
        const trOAM = document.getElementById('tr-oam').value

        const toaData = [];

        for (const tech of technologies) {
            if (tech === '4G') {
                const trS1 = document.getElementById('tr-s1').value;
                const selectedBands4g = [];
                const bands4gCheckboxes = document.querySelectorAll('input[name="4g_band"]:checked');
                bands4gCheckboxes.forEach(checkbox=>{
                    selectedBands4g.push(checkbox.value)
                });
                selectedBands4g.forEach(band => {
                    toaData.push({
                        'band': band,
                        'toa-date': toaDate,
                        'technology': '4G',
                        'sitename': sitename,
                        'network': subNetwork,
                        'cabinet': cabinetValue,
                        'sn': serialNumber,
                        'employer': acceptedValue,
                        'tr-ip': trS1,
                        'oam-ip': trOAM,
                        'kato': KATO,
                        'address': address,
                        'latitude': latitude,
                        'longitude': longitude,
                    })
                });
            } else if (tech === '5G') {
                const trNR = document.getElementById('tr-nr').value;
                const selectedBands5g = [];
                const bands5gCheckboxes = document.querySelectorAll('input[name="5g_band"]:checked');
                bands5gCheckboxes.forEach(checkbox=>{
                    selectedBands5g.push(checkbox.value)
                });
                selectedBands5g.forEach(band => {
                    toaData.push({
                        'band': band,
                        'toa-date': toaDate,
                        'technology': '5G',
                        'sitename': sitename,
                        'network': subNetwork,
                        'cabinet': cabinetValue,
                        'sn': serialNumber,
                        'employer': acceptedValue,
                        'tr-ip': trNR,
                        'oam-ip': trOAM,
                        'kato': KATO,
                        'address': address,
                        'latitude': latitude,
                        'longitude': longitude,
                    })
                });

            } else if (tech === '2G') {
                const sitename2G = await get2GSiteName(sitename);
                const LAC = document.getElementById('2g_data_lac').value;
                const NE2G = document.getElementById('2g_data_ne').value;
                const CellList = document.getElementById('2g_data_cell_list').value;
                const CIList = document.getElementById('2g_data_CI_list').value;
                const TG = document.getElementById('2g_data_tg').value;
                const TRX = document.getElementById('2g_data_trx').value;
                const EDGE = document.getElementById('2g_data_edge').value;
                const trAbis = document.getElementById('tr-abis').value;

                toaData.push({
                    'toa-date': toaDate,
                    'technology': '2G',
                    'sitename': sitename2G,
                    'STG': TG,
                    'NE': NE2G,
                    'celllist': CellList,
                    'LAC': LAC,
                    'CIList': CIList,
                    'TRX': TRX,
                    'EDGE': EDGE,
                    'cabinet': cabinetValue,
                    'sn': serialNumber,
                    'employer': acceptedValue,
                    'tr-ip': trAbis,
                    'kato': KATO,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                });

            } else if (tech === '3G') {
                const LAC = document.getElementById('3g_data_lac').value;
                const NE = document.getElementById('3g_data_ne').value;
                const CellList = document.getElementById('3g_data_cell_list').value;
                const CIList = document.getElementById('3g_data_CI_list').value;
                const trIUB = document.getElementById('tr-iub').value;
                toaData.push({
                    'toa-date': toaDate,
                    'technology': '3G',
                    'sitename': sitename,
                    'NE': NE,
                    'celllist': CellList,
                    'LAC': LAC,
                    'CIList': CIList,
                    'cabinet': cabinetValue,
                    'sn': serialNumber,
                    'employer': acceptedValue,
                    'tr-ip': trIUB,
                    'tr-oam': trOAM,
                    'kato': KATO,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                });
            }
        }

        if (toaData.length === 0) {
            console.error("Ошибка: TOA Data пустой, отправка отменена!");
            return;
        }

        formData.append('toaData', JSON.stringify(toaData))

        const csrfToken = $('[name=csrfmiddlewaretoken]').val();
        fetch('/toa_submit/create/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (!data.data) {
                console.error("Ошибка: сервер не вернул данные!", data);
                return;
            }

            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-info';
            alertDiv.style.position = 'fixed';
            alertDiv.style.top = '20px';
            alertDiv.style.right = '20px';
            alertDiv.style.width = '300px';
            alertDiv.style.padding = '15px';
            alertDiv.style.borderRadius = '4px';
            alertDiv.style.backgroundColor = '#d9edf7';
            alertDiv.style.color = '#31708f';
            alertDiv.style.zIndex = '1000';
            alertDiv.innerHTML = '<strong>Results:</strong><br>';

            data.data.forEach(item => {
                const resultText = `Technology: ${item.technology}, Band: ${item.band}, Status: ${item.success}`;
                const resultDiv = document.createElement('div');
                resultDiv.innerText = resultText;
                alertDiv.appendChild(resultDiv);
            });

            document.body.appendChild(alertDiv);
            setTimeout(() => {
                alertDiv.remove();
            }, 4000);

            setTimeout(() => {
                window.location.href = data.redirect_url;
            }, 4000);

        })
        .catch(error => console.error('Error:', error));
});