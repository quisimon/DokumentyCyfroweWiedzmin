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
            const formData = {
                witcher_contract: {
                    date_and_location: document.querySelector('input[name="data_i_miejscowość"]').value || "",
                    contractor: {
                        first_name: document.querySelector('input[name="imię"]').value || "",
                        last_name: document.querySelector('input[name="nazwisko"]').value || "",
                        gender: document.querySelector('input[name="płeć"]:checked')?.value || "",
                        place_of_residence: document.querySelector('input[name="residence"]:checked')?.value || "",
                        residence_details: {
                            name_of_location: document.querySelector('input[name="nazwa_miasta"], input[name="nazwa_wsi"]')?.value || "",
                            occupation: document.querySelector('input[name="zajęcie"]')?.value || "",
                            guild: document.querySelector('input[name="reprezentowany_cech_lub_gildia"]')?.value || "",
                            contact_person: document.querySelector('input[name="adres_kontaktowy_sołtysa_lub_lokalnego_kapłana"]')?.value || "",
                            contact_address: document.querySelector('input[name="ulica"]')?.value + " " + document.querySelector('input[name="mieszkanie"]')?.value || ""
                        }
                    },
                    witcher: {
                        name: document.querySelector('input[name="imię_lub_przydomek"]').value || "",
                        school: document.querySelector('input[name="szkoła_wiedźmińska"]').value || ""
                    },
                    contract_details: {
                        // Changed select[] to input[]
                        monster_species: document.querySelector('input[name="gatunek_potwora"]').value || "",
                        // Changed textarea[] to input[]
                        monster_details: document.querySelector('input[name="opis_potwora"]').value || "",
                        operation_area: document.querySelector('input[name="obszar_działania"]').value || "",
                        previous_victims: {
                            killed: parseInt(document.querySelector('input[name="zabici"]')?.value || "0"),
                            injured: parseInt(document.querySelector('input[name="ranni"]')?.value || "0")
                        },
                        // Changed textarea[] to input[]
                        additional_information: document.querySelector('input[name="informacje_dodatkowe"]').value || "",
                        contract_amount: {
                            currency: document.querySelector('input[name="waluta"]').value || "",
                            amount: parseFloat(document.querySelector('input[name="kwota"]').value || "0"),
                            advance: parseFloat(document.querySelector('input[name="zaliczka"]').value || "0")
                        }
                    },
                    signatures: {
                        contractor: document.querySelector('input[name="podpis_zlecającego"]').value || "",
                        witcher: document.querySelector('input[name="podpis_wiedźmina"]').value || ""
                    }
                }
            };
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