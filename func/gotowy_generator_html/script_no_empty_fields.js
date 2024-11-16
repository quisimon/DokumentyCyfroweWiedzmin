// Show/hide fields based on residence choice"
        document.querySelectorAll('input[name=\"residence\"]').forEach(radio => {
            radio.addEventListener('change', function() {
                document.getElementById('cityData').style.display = this.value === 'Miasto' ? 'block' : 'none';
                document.getElementById('villageData').style.display = this.value === 'Wieś' ? 'block' : 'none';
            });
        });
        // Show/hide monster description based on monster type
        document.addEventListener('DOMContentLoaded', function() {
            const monsterTypeDropdown = document.getElementById('monsterType');
            const monsterDescriptionDiv = document.getElementById('monsterDescription');
            monsterTypeDropdown.addEventListener('change', function() {
                if (this.value === 'Niezidentyfikowany') {
                    monsterDescriptionDiv.style.display = 'block';
                } else {
                    monsterDescriptionDiv.style.display = 'none';
                }
            });
        });
        // Function to gather form data and convert to JSON
        function gatherFormData() {
            // Helper function to get the value of an input or return null if empty
            function getFieldValue(selector) {
                const element = document.querySelector(selector);
                return element && element.value.trim() ? element.value.trim() : null;
            }

            // Helper function for radio buttons
            function getSelectedRadioValue(name) {
                const radio = document.querySelector(`input[name="${name}"]:checked`);
                return radio ? radio.value : null;
            }

            // Start creating JSON structure
            const formData = {
                witcher_contract: {
                    date_and_location: null,
                    contractor: null,
                    witcher: null,
                    contract_details: null,
                    signatures: {
                        contractor: null,
                        witcher: null
                    }
                }
            };

            // Add date and location
            formData.witcher_contract.date_and_location = getFieldValue('input[name="data_i_miejscowość"]') || "";

            // Add contractor details
            const contractor = {
                first_name: getFieldValue('input[name="imię"]'),
                last_name: getFieldValue('input[name="nazwisko"]'),
                gender: getSelectedRadioValue('płeć'),
                place_of_residence: getSelectedRadioValue('residence'),
                residence_details: {
                    name_of_location: null,
                    contact_address: {
                        street: null,
                        house_number: null
                    },
                    occupation: null,
                    guild: null
                }
            };

            // Add residence-specific details (city or village)
            if (contractor.place_of_residence === 'Miasto') {
                contractor.residence_details.name_of_location = getFieldValue('input[name="nazwa_miasta"]');
                contractor.residence_details.contact_address.street = getFieldValue('input[name="ulica"]');
                contractor.residence_details.contact_address.house_number = getFieldValue('input[name="mieszkanie"]');
                contractor.residence_details.occupation = getFieldValue('input[name="zatrudnienie"]');
                contractor.residence_details.guild = getFieldValue('input[name="reprezentowany_cech_lub_gildia"]');
            } else if (contractor.place_of_residence === 'Wieś') {
                contractor.residence_details.name_of_location = getFieldValue('input[name="nazwa_wsi"]');
                contractor.residence_details.occupation = getFieldValue('input[name="zajęcie"]');
                contractor.residence_details.contact_address = getFieldValue('input[name="adres_kontaktowy_sołtysa_lub_lokalnego_kapłana"]');
            }

            // Only add contractor if at least one field is filled
            if (Object.values(contractor).some(value => value)) {
                formData.witcher_contract.contractor = contractor;
            }

            // Add witcher details
            const witcher = {
                name: getFieldValue('input[name="imię_lub_przydomek"]'),
                school: getFieldValue('input[name="szkoła_wiedźmińska"]')
            };
            if (Object.values(witcher).some(value => value)) {
                formData.witcher_contract.witcher = witcher;
            }

            // Add contract details
            const contractDetails = {
                monster_species: getFieldValue('input[name="gatunek_potwora"]'),
                monster_details: getFieldValue('input[name="opis_potwora"]'),
                operation_area: getFieldValue('input[name="obszar_działania"]'),
                previous_victims: getFieldValue('input[name="dotychczasowe_ofiary"]') || 0,
                additional_information: getFieldValue('input[name="informacje_dodatkowe"]'),
                contract_amount: {
                    currency: getFieldValue('input[name="waluta"]'),
                    amount: parseFloat(getFieldValue('input[name="kwota"]')) || 0,
                    advance: parseFloat(getFieldValue('input[name="zaliczka"]')) || 0
                }
            };

            // Only add contract details if at least one field is filled
            if (Object.values(contractDetails).some(value => value)) {
                formData.witcher_contract.contract_details = contractDetails;
            }

            // Add signatures
            formData.witcher_contract.signatures.contractor = getFieldValue('input[name="podpis_zlecającego"]');
            formData.witcher_contract.signatures.witcher = getFieldValue('input[name="podpis_wiedźmina"]');

            // Return the JSON object
            return JSON.stringify(formData, null, 2);
        }

        // Save data to json file
        function saveJsonFile(data, filename = 'daneZlecenia.json') {
            const blob = new Blob([data], { type: 'application/json' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
        }

        document.getElementById('submitBtn').addEventListener('click', function() {
            const formDataJson = gatherFormData();
            saveJsonFile(formDataJson)
            alert('Formularz został zapisany!');
        })