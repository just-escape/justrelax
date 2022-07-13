<template>
  <div>
    <div class="d-flex flex-row justify-content-end">
      <div class="d-flex justify-content-end">
        <div class="min-width-100px mr-1 mb-1">
          <b-form-select
            class="form-control"
            v-model="selected"
            :options="{
              'd1.scenario': 'Digimiam zone 1',
              'd2.scenario': 'Digimiam zone 2',
              'digimiam.scenario': 'Digimiam zone 1 et 2',
            }"
            :html="true"
          />
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <div class="row">
        <div
          v-for="card in cards.filter(card => card.roomIds.includes(roomId))"
          :key="card.id"
          class="col-12 col-lg-6 col-xl-3 mb-1 px-1"
        >
          <ActionCard
            :roomId="roomId"
            :card="card"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ActionCard from '@/components/live/ActionCard.vue'
import roomStore from '@/store/roomStore.js'

export default {
  name: 'Actions',
  components: {
    ActionCard
  },
  data() {
    return {
      cards: [
        {
          "id": 4,
          "name": "Contrôle",
          "index": 0,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 381,
              "card": 4,
              "name": "Baguettes",
              "index": 0,
              "maintenance": false,
              "widget": "chopsticks",
              "widget_params": ""
            },
            {
              "id": 113,
              "card": 4,
              "name": "Status",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "control_set_status_inactive",
                  "icon": "fa-fw fas fa-lock"
                },
                {
                  "id": "control_set_status_playing",
                  "icon": "fa-fw fas fa-gamepad"
                }
              ]
            },
            {
              "id": 8,
              "card": 4,
              "name": "Table",
              "index": 4,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "control_table_up",
                  "icon": "fa-fw fas fa-arrow-up"
                },
                {
                  "id": "control_table_down",
                  "icon": "fa-fw fas fa-arrow-down"
                },
                {
                  "id": "control_table_stop",
                  "icon": "fa-fw far fa-hand-paper"
                }
              ]
            },
            {
              "id": 116,
              "card": 4,
              "name": "Force manual mode",
              "index": 5,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "control_force_manual_mode",
                  "icon": "fa-fw fas fa-plug"
                }
              ]
            },
            {
              "id": 382,
              "card": 4,
              "name": "Rappel CONTROL",
              "index": 7,
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "chopsticks_voice_clue_1",
                "execute_help": "Je vous rappelle que vous devez acceder au pannel de controle pour désactiver le marmitron."
              }
            },
            {
              "id": 383,
              "card": 4,
              "name": "Tige pour CONTROL",
              "index": 8,
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "chopsticks_voice_clue_2",
                "execute_help": "Le logiciel de maintenance indique que vous avez besoin d'une tige pour enclencher les mécanismes du panel de contrôle."
              }
            },
            {
              "id": 353,
              "card": 4,
              "name": "Configurez lumières",
              "index": 9,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_3",
                    "localized": true
                  },
                  "help": "Configurez la bonne combinaison de couleur des lumières pour ouvrir le pannel de contrôle."
                }
              ]
            },
            {
              "id": 354,
              "card": 4,
              "name": "Passez en mode manuel",
              "index": 10,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_4",
                    "localized": true
                  },
                  "help": "N'oubliez pas de passer le restaurant en mode manuel grâce au câble de contrôle !"
                }
              ]
            },
            {
              "id": 384,
              "card": 4,
              "name": "Panel de contrôle",
              "index": 20,
              "maintenance": false,
              "widget": "control_panel",
              "widget_params": ""
            }
          ]
        },
        {
          "id": 1,
          "name": "Lumières",
          "index": 1,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 2,
              "card": 1,
              "name": "Blanc",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "white"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "white"
                  }
                }
              ]
            },
            {
              "id": 3,
              "card": 1,
              "name": "Bleu",
              "index": 3,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights_glitch",
                  "icon": "fa-fw fas fa-cloud-sun-rain",
                  "extra": {
                    "color": "blue"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights_stop_glitch",
                  "icon": "fa-fw fas fa-check",
                  "extra": {
                    "color": "blue"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "blue"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "blue"
                  }
                }
              ]
            },
            {
              "id": 4,
              "card": 1,
              "name": "Orange",
              "index": 4,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights_glitch",
                  "icon": "fa-fw fas fa-cloud-sun-rain",
                  "extra": {
                    "color": "orange"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights_stop_glitch",
                  "icon": "fa-fw fas fa-check",
                  "extra": {
                    "color": "orange"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "orange"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "orange"
                  }
                }
              ]
            },
            {
              "id": 5,
              "card": 1,
              "name": "Vert",
              "index": 5,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights_glitch",
                  "icon": "fa-fw fas fa-cloud-sun-rain",
                  "extra": {
                    "color": "green"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights_stop_glitch",
                  "icon": "fa-fw fas fa-check",
                  "extra": {
                    "color": "green"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "green"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "green"
                  }
                }
              ]
            },
            {
              "id": 6,
              "card": 1,
              "name": "Rouge",
              "index": 6,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights_glitch",
                  "icon": "fa-fw fas fa-cloud-sun-rain",
                  "extra": {
                    "color": "red"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights_stop_glitch",
                  "icon": "fa-fw fas fa-check",
                  "extra": {
                    "color": "red"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "red"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "red"
                  }
                }
              ]
            },
            {
              "id": 7,
              "card": 1,
              "name": "Rose",
              "index": 7,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights_glitch",
                  "icon": "fa-fw fas fa-cloud-sun-rain",
                  "extra": {
                    "color": "pink"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights_stop_glitch",
                  "icon": "fa-fw fas fa-check",
                  "extra": {
                    "color": "pink"
                  },
                  "maintenance": true
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "pink"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "pink"
                  }
                }
              ]
            },
            {
              "id": 338,
              "card": 1,
              "name": "Calibration dalles",
              "index": 8,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "load_cells_calibrate",
                  "icon": "fa-fw fas fa-balance-scale"
                }
              ]
            },
            {
              "id": 339,
              "card": 1,
              "name": "Lumières désactivées",
              "index": 9,
              "maintenance": false,
              "widget": "synchronizer_lights",
              "widget_params": ""
            }
          ]
        },
        {
          "id": 52,
          "name": "Écran synchro",
          "index": 3,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 265,
              "card": 52,
              "name": "Status",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "reset_synchronizer",
                  "icon": "fa-fw fas fa-undo-alt"
                },
                {
                  "id": "synchronizer_restaurant_in_manual_mode",
                  "icon": "fa-fw fas fa-gamepad"
                }
              ]
            },
            {
              "id": 402,
              "card": 52,
              "name": "Synchronizer",
              "index": 0,
              "maintenance": false,
              "widget": "synchronizer",
              "widget_params": ""
            },
            {
              "id": 311,
              "card": 52,
              "name": "Overlay vidéo",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "synchronizer_overlay_video_glitch",
                  "icon": "fa-fw fas fa-dice-one",
                  "maintenance": true
                },
                {
                  "id": "synchronizer_overlay_video_ads",
                  "icon": "fa-fw fas fa-dice-two",
                  "maintenance": true
                },
                {
                  "id": "stop_synchronizer_overlay_video",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 301,
              "card": 52,
              "name": "Menu : slide",
              "index": 3,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "part": "slide",
                    "slide": 0
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-dice-two",
                  "extra": {
                    "part": "slide",
                    "slide": 1
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-dice-three",
                  "extra": {
                    "part": "slide",
                    "slide": 2
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-dice-four",
                  "extra": {
                    "part": "slide",
                    "slide": 3
                  }
                }
              ]
            },
            {
              "id": 302,
              "card": 52,
              "name": "Menu : X",
              "index": 4,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-drumstick-bite",
                  "extra": {
                    "part": "x",
                    "x": 0
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-pizza-slice",
                  "extra": {
                    "part": "x",
                    "x": 1
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-stroopwafel",
                  "extra": {
                    "part": "x",
                    "x": 2
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-glass-whiskey",
                  "extra": {
                    "part": "x",
                    "x": 3
                  }
                }
              ]
            },
            {
              "id": 303,
              "card": 52,
              "name": "Menu : Y",
              "index": 5,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-seedling",
                  "extra": {
                    "part": "y",
                    "y": 0
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-search",
                  "extra": {
                    "part": "y",
                    "y": 1
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-bug",
                  "extra": {
                    "part": "y",
                    "y": 2
                  }
                },
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-smile",
                  "extra": {
                    "part": "y",
                    "y": 3
                  }
                }
              ]
            },
            {
              "id": 304,
              "card": 52,
              "name": "Menu : error",
              "index": 7,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "holomenu_set_part",
                  "icon": "fa-fw fas fa-exclamation-triangle",
                  "extra": {
                    "part": "error"
                  }
                }
              ]
            },
            {
              "id": 312,
              "card": 52,
              "name": "Succès forcé",
              "index": 8,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "synchronizer_success_lights",
                  "icon": "fa-fw fas fa-sun"
                },
                {
                  "id": "synchronizer_success_menu",
                  "icon": "fa-fw fas fa-utensils"
                }
              ]
            },
            {
              "id": 317,
              "card": 52,
              "name": "Log lumières",
              "index": 12,
              "maintenance": false,
              "widget": "log_prompt",
              "widget_params": {
                "id": "light_log",
                "preset_messages": [
                  {
                    "value": {
                      "message": "lights_have_been_reset",
                      "level": "warning"
                    },
                    "text": "Réinitialisation des lumières"
                  },
                  {
                    "value": {
                      "message": "lights_have_been_turned_off",
                      "level": "info"
                    },
                    "text": "Extinction de toutes les lumières"
                  },
                  {
                    "value": {
                      "message": "lights_can_be_turned_on_manually",
                      "level": "info"
                    },
                    "text": "Les lumières peuvent être allumées manuellement"
                  },
                  {
                    "value": {
                      "message": "waiting_lights_to_be_resync",
                      "level": "info"
                    },
                    "text": "En attente de la resynchronisation"
                  },
                  {
                    "value": {
                      "message": "interface_is_not_tactile",
                      "level": "warning"
                    },
                    "text": "Les lumières ne peuvent pas être allumées avec l'écran tactile"
                  },
                  {
                    "value": {
                      "message": "floor_switches_are_idle",
                      "level": "info"
                    },
                    "text": "Les interrupteurs au sol sont en attente d'activation"
                  },
                  {
                    "value": {
                      "message": "pink_clue",
                      "level": "info"
                    },
                    "text": "Le rose doit être allumé de manière appropriée"
                  },
                  {
                    "value": {
                      "message": "light_sync_complete",
                      "level": "info"
                    },
                    "text": "Synchronisation des lumières terminée"
                  }
                ]
              }
            },
            {
              "id": 318,
              "card": 52,
              "name": "Log menu",
              "index": 13,
              "maintenance": false,
              "widget": "log_prompt",
              "widget_params": {
                "id": "menu_log",
                "preset_messages": [
                  {
                    "value": {
                      "message": "menu_is_messed_up",
                      "level": "warning"
                    },
                    "text": "Réinitialisation complète du menu"
                  },
                  {
                    "value": {
                      "message": "waiting_dishes_to_be_configured",
                      "level": "info"
                    },
                    "text": "En attente de la reconfiguration des plats du Digimiam"
                  },
                  {
                    "value": {
                      "message": "dishes_need_to_have_good_prices",
                      "level": "warning"
                    },
                    "text": "Le Digimiam ne peut pas se permettre de vendre ces plats à ces prix-là"
                  },
                  {
                    "value": {
                      "message": "some_dishes_cannot_be_produced",
                      "level": "warning"
                    },
                    "text": "Certains plats ne correspondent pas à la carte du Digimiam"
                  },
                  {
                    "value": {
                      "message": "no_dishes_can_be_produced",
                      "level": "warning"
                    },
                    "text": "Aucun de ces plats ne correspond à la carte du Digimiam"
                  },
                  {
                    "value": {
                      "message": "menu_reconfig_complete",
                      "level": "info"
                    },
                    "text": "Reconfiguration des plats terminée"
                  }
                ]
              }
            },
            {
              "id": 355,
              "card": 52,
              "name": "Indications utiles à lire",
              "index": 30,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_5",
                    "localized": true
                  },
                  "help": "L'écran de maintenance donne des indications qui peuvent se révèler utiles à lire."
                }
              ]
            },
            {
              "id": 356,
              "card": 52,
              "name": "Retrouvez les plats/prix",
              "index": 31,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_6",
                    "localized": true
                  },
                  "help": "Ce satané Marmitron a déréglé le menu du Digimiam, en cherchant dans le restaurant vous deriez retrouver les plats du menu et leur prix."
                }
              ]
            },
            {
              "id": 357,
              "card": 52,
              "name": "Emballages dans la poubelle",
              "index": 32,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_7",
                    "localized": true
                  },
                  "help": "Êtes-vous sûr d'avoir trouvé tous les plats du restaurant ? Les emballages dans la poubelle pourraient vous aider."
                }
              ]
            },
            {
              "id": 358,
              "card": 52,
              "name": "Il reste des tickets de caisse",
              "index": 33,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_8",
                    "localized": true
                  },
                  "help": "Êtes-vous sûr d'avoir trouvé tous les plats du restaurant ? Il doit bien rester des tickets de caisse !"
                }
              ]
            },
            {
              "id": 359,
              "card": 52,
              "name": "Aidez-vous des pubs",
              "index": 34,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_9",
                    "localized": true
                  },
                  "help": "Êtes-vous sûr d'avoir trouvé tous les plats du restaurant ? Aidez-vous des publicités !"
                }
              ]
            },
            {
              "id": 360,
              "card": 52,
              "name": "Regardez sous vos pieds",
              "index": 35,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_10",
                    "localized": true
                  },
                  "help": "Les interrupteurs de synchronisation des lumières sont situés dans la salle, regardez bien sous vos pieds !"
                }
              ]
            },
            {
              "id": 361,
              "card": 52,
              "name": "Concentrez-vous sur 1 lumière",
              "index": 36,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_11",
                    "localized": true
                  },
                  "help": "Le restaurant n'a pas assez de puissance pour synchroniser toutes les lumières simultanément, concentrez-vous sur une lumière à la fois pour aller plus vite."
                }
              ]
            }
          ]
        },
        {
          "id": 29,
          "name": "Rue / publicités",
          "index": 4,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 272,
              "card": 29,
              "name": "Vidéo Marmitron",
              "index": 0,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "advertiser_play_street_idle",
                  "icon": "fa-fw fas fa-video"
                },
                {
                  "id": "advertiser_stop_street_idle",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 273,
              "card": 29,
              "name": "Vidéo publicité glitchée",
              "index": 1,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "advertiser_play_ads_glitch",
                  "icon": "fa-fw fas fa-video"
                },
                {
                  "id": "advertiser_stop_ads_glitch",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 329,
              "card": 29,
              "name": "Vidéo pub gaufresque",
              "index": 2,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "advertiser_play_waffresco_ad_loop",
                  "icon": "fa-fw fas fa-video"
                },
                {
                  "id": "advertiser_stop_waffresco_ad_loop",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 274,
              "card": 29,
              "name": "Vidéo pubs",
              "index": 3,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "advertiser_play_ads_loop",
                  "icon": "fa-fw fas fa-video"
                },
                {
                  "id": "advertiser_stop_ads_loop",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 275,
              "card": 29,
              "name": "Vidéo Mme Poivre",
              "index": 4,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "advertiser_play_ms_pepper_here_you_are",
                  "icon": "fa-fw fas fa-video"
                },
                {
                  "id": "advertiser_stop_ms_pepper_here_you_are",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 276,
              "card": 29,
              "name": "Interface menu",
              "index": 5,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "street_display_reset",
                  "icon": "fa-fw fas fa-undo-alt"
                }
              ]
            },
            {
              "id": 277,
              "card": 29,
              "name": "Porte",
              "index": 6,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "front_door_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "front_door_close",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 300,
              "card": 29,
              "name": "Lumières rue",
              "index": 7,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "street_lights_glitch",
                  "icon": "fa-fw fas fa-cloud-sun-rain",
                  "maintenance": true
                },
                {
                  "id": "street_lights_stop_glitch",
                  "icon": "fa-fw fas fa-check",
                  "maintenance": true
                },
                {
                  "id": "street_lights_on",
                  "icon": "fa-fw far fa-sun"
                },
                {
                  "id": "street_lights_off",
                  "icon": "fa-fw fas fa-power-off"
                }
              ]
            }
          ]
        },
        {
          "id": 53,
          "name": "Écran commandes",
          "index": 5,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 11,
              "card": 53,
              "name": "Status",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "reset_orders",
                  "icon": "fa-fw fas fa-undo-alt"
                },
                {
                  "id": "stop_orders_overlay_video",
                  "icon": "fa-fw fas fa-video-slash"
                }
              ]
            },
            {
              "id": 307,
              "card": 53,
              "name": "Module de paiement",
              "index": 6,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "payment_authenticate",
                  "icon": "fa-fw fas fa-ring"
                },
                {
                  "id": "payment_cancel_authentication",
                  "icon": "fa-fw fas fa-ban"
                },
                {
                  "id": "payment_status",
                  "icon": "fa-fw fas fa-gamepad",
                  "extra": {
                    "status": "playing"
                  }
                },
                {
                  "id": "payment_status",
                  "icon": "fa-fw fas fa-times",
                  "extra": {
                    "status": "disabled"
                  }
                }
              ]
            },
            {
              "id": 319,
              "card": 53,
              "name": "Instruction doc ventil",
              "index": 8,
              "maintenance": false,
              "widget": "instruction_prompt",
              "widget_params": {
                "id": "ventilation_documentation_log",
                "preset_messages": [
                  {
                    "value": {
                      "message": "display_instructions",
                      "loop": false
                    },
                    "text": "Lancez les instructions"
                  },
                  {
                    "value": {
                      "message": "unplug_before_intervention",
                      "loop": false
                    },
                    "text": "Débranchez les conduits avant de procéder à l'intervention"
                  },
                  {
                    "value": {
                      "message": "all_sequences_are_correct",
                      "loop": false
                    },
                    "text": "Toutes les séquences sont correctes"
                  },
                  {
                    "value": {
                      "message": "order_matters",
                      "loop": false
                    },
                    "text": "L'ordre des instructions doit être respecté"
                  },
                  {
                    "value": {
                      "message": "digimiam_ducts_can_now_be_used",
                      "loop": false
                    },
                    "text": "Les circuits d'aération du Digimiam sont maintenant pratiquables"
                  }
                ]
              }
            },
            {
              "id": 369,
              "card": 53,
              "name": "Transférez néofrancs bague",
              "index": 100,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_1",
                    "localized": true
                  },
                  "help": "Vous pouvez transférer des néofrancs grâce à votre bague sur le terminal d'identification."
                }
              ]
            },
            {
              "id": 362,
              "card": 53,
              "name": "Commande hauteur moyen",
              "index": 101,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_12",
                    "localized": true
                  },
                  "help": "Vous devriez peut-être réaliser une commande à la hauteur de vos moyens..."
                }
              ]
            }
          ]
        },
        {
          "id": 2,
          "name": "Ventilation",
          "index": 6,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 405,
              "card": 2,
              "name": "Ignorer le panel de ventilation",
              "index": 0,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "ventilation_panel_skip"
              }
            },
            {
              "id": 406,
              "card": 2,
              "name": "Timer ignorer le panel",
              "index": 0,
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "ventilation_panel_skip_timer",
                "execute_help": "Ignore automatiquement le panel de ventilation."
              }
            },
            {
              "id": 323,
              "card": 2,
              "name": "Conduit",
              "index": 3,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "vents_locker",
                  "icon": "fa-fw fas fa-lock-open",
                  "extra": {
                    "lock": false
                  }
                },
                {
                  "id": "vents_locker",
                  "icon": "fa-fw fas fa-lock",
                  "extra": {
                    "lock": true
                  }
                }
              ]
            },
            {
              "id": 363,
              "card": 2,
              "name": "Module de ventilation",
              "index": 10,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_13",
                    "localized": true
                  },
                  "help": "Vous devez ouvrir la trappe de ventilation grâce au module situé en haut à gauche de celle-ci."
                }
              ]
            },
            {
              "id": 364,
              "card": 2,
              "name": "Plus vite plus loin",
              "index": 11,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_14",
                    "localized": true
                  },
                  "help": "Seul on va plus vite, ensemble on va plus loin."
                }
              ]
            },
            {
              "id": 407,
              "card": 2,
              "name": "Ventilation",
              "index": 20,
              "maintenance": false,
              "widget": "ventilation_panel",
              "widget_params": ""
            }
          ]
        },
        {
          "id": 51,
          "name": "Stock",
          "index": 7,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 257,
              "card": 51,
              "name": "Lumières",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "stock_lights_high",
                  "icon": "fa-fw far fa-sun"
                },
                {
                  "id": "stock_lights_low",
                  "icon": "fa-fw far fa-moon"
                },
                {
                  "id": "stock_lights_off",
                  "icon": "fa-fw fas fa-power-off"
                }
              ]
            },
            {
              "id": 258,
              "card": 51,
              "name": "Fermer les portes stock/serveurs",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "emergency_exit_lock",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 408,
              "card": 51,
              "name": "Porte vers l'extérieur",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "emergency_exit_unlock_to_outside",
                  "icon": "fa-fw fas fa-lock-open"
                }
              ]
            },
            {
              "id": 409,
              "card": 51,
              "name": "Porte stock<->salle serveurs",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "emergency_exit_unlock_stock_to_machine",
                  "icon": "fa-fw fas fa-lock-open"
                }
              ]
            },
            {
              "id": 404,
              "card": 51,
              "name": "Cylindres",
              "index": 2,
              "maintenance": false,
              "widget": "cylinders",
              "widget_params": ""
            },
            {
              "id": 352,
              "card": 51,
              "name": "Cylindres check",
              "index": 3,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "id": "potjevleesch"
                  }
                },
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-two",
                  "extra": {
                    "id": "salade_flamande"
                  }
                },
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-three",
                  "extra": {
                    "id": "cambraisienne"
                  }
                },
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-four",
                  "extra": {
                    "id": "gaufresque"
                  }
                }
              ]
            },
            {
              "id": 365,
              "card": 51,
              "name": "Enclenchement rotation",
              "index": 10,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_15",
                    "localized": true
                  },
                  "help": "Le logiciel de maintenance indique que les capsules alimentaires doivent être enclenchées grâce à une rotation dans le sens horaire."
                }
              ]
            },
            {
              "id": 368,
              "card": 51,
              "name": "Rdv dans le réfectoire",
              "index": 12,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_18",
                    "localized": true
                  },
                  "help": "Le stock alimentaire est fonctionnel. Rendez-vous dans le réfectoire du restaurant pour relancer la commande de test."
                }
              ]
            }
          ]
        },
        {
          "id": 3,
          "name": "Sokoban",
          "index": 8,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 12,
              "card": 3,
              "name": "Reset (énigme entière)",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "reset_inventory",
                  "icon": "fa-fw fas fa-undo-alt"
                },
                {
                  "id": "inventory_black_screen",
                  "icon": "fa-fw fas fa-video",
                  "extra": {
                    "display": false
                  }
                },
                {
                  "id": "inventory_black_screen",
                  "icon": "fa-fw fas fa-video-slash",
                  "extra": {
                    "display": true
                  },
                  "maintenance": true
                }
              ]
            },
            {
              "id": 219,
              "card": 3,
              "name": "Contrôles (1/2)",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "sokoban_control_up",
                  "icon": "fa-fw fas fa-chevron-up"
                },
                {
                  "id": "sokoban_control_reset",
                  "icon": "fa-fw fas fa-undo-alt"
                }
              ]
            },
            {
              "id": 220,
              "card": 3,
              "name": "Contrôles (2/2)",
              "index": 3,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "sokoban_control_left",
                  "icon": "fa-fw fas fa-chevron-left"
                },
                {
                  "id": "sokoban_control_down",
                  "icon": "fa-fw fas fa-chevron-down"
                },
                {
                  "id": "sokoban_control_right",
                  "icon": "fa-fw fas fa-chevron-right"
                }
              ]
            },
            {
              "id": 320,
              "card": 3,
              "name": "Log inventaire",
              "index": 5,
              "maintenance": false,
              "widget": "log_prompt",
              "widget_params": {
                "id": "inventory_log",
                "preset_messages": [
                  {
                    "value": {
                      "message": "a",
                      "level": "info"
                    },
                    "text": "a"
                  },
                  {
                    "value": {
                      "message": "b",
                      "level": "warning"
                    },
                    "text": "b"
                  }
                ]
              }
            },
            {
              "id": 366,
              "card": 3,
              "name": "Déplacez-vous deuxième niveau",
              "index": 10,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_16",
                    "localized": true
                  },
                  "help": "Vous n'avez pas fini d'organiser les capsules virtuelles, déplacez-vous dans le deuxième niveau grâce à la flèche."
                }
              ]
            },
            {
              "id": 367,
              "card": 3,
              "name": "Logiciel aide orga virtuelle",
              "index": 11,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "pepper_17",
                    "localized": true
                  },
                  "help": "Le logiciel de maintenance va vous donner un coup de pouce pour organiser les capsules virtuelles."
                }
              ]
            },
            {
              "id": 397,
              "card": 3,
              "name": "Sokoban",
              "index": 20,
              "maintenance": false,
              "widget": "sokoban",
              "widget_params": ""
            }
          ]
        },
        {
          "id": 54,
          "name": "Usine à gaufres",
          "index": 9,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 280,
              "card": 54,
              "name": "Lumière Niryo",
              "index": 6,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_light",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "led_id": "niryo",
                    "on": true
                  }
                },
                {
                  "id": "waffle_factory_light",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "led_id": "niryo",
                    "on": false
                  }
                }
              ]
            },
            {
              "id": 285,
              "card": 54,
              "name": "Lumière imprimante",
              "index": 7,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_light",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "led_id": "printer",
                    "on": true
                  }
                },
                {
                  "id": "waffle_factory_light",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "led_id": "printer",
                    "on": false
                  }
                }
              ]
            },
            {
              "id": 284,
              "card": 54,
              "name": "Trappe",
              "index": 8,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "waffle_trapdoor_close",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 395,
              "card": 54,
              "name": "Verouillage trappe",
              "index": 8,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "input_device",
                "key": "waffle_limit_switch"
              }
            },
            {
              "id": 298,
              "card": 54,
              "name": "Four",
              "index": 11,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "oven_turn_off",
                  "icon": "fa-fw fas fa-ban"
                },
                {
                  "id": "oven_turn_on",
                  "icon": "fa-fw fas fa-fire-alt"
                }
              ]
            },
            {
              "id": 305,
              "card": 54,
              "name": "Niryo aimant",
              "index": 12,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "niryo_magnetize",
                  "icon": "fa-fw fas fa-ban",
                  "extra": {
                    "value": false
                  }
                },
                {
                  "id": "niryo_magnetize",
                  "icon": "fa-fw fas fa-magnet",
                  "extra": {
                    "value": true
                  }
                }
              ]
            },
            {
              "id": 386,
              "card": 54,
              "name": "Niryo animations",
              "index": 12,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "niryo_animation",
                  "icon": "fa-fw fas fa-link",
                  "extra": {
                    "animation": "animation"
                  }
                },
                {
                  "id": "niryo_animation",
                  "icon": "fa-fw fas fa-unlink",
                  "extra": {
                    "animation": "bugged_animation"
                  }
                },
                {
                  "id": "niryo_animation",
                  "icon": "fa-fw fas fa-arrow-alt-circle-left",
                  "extra": {
                    "animation": "back_to_base"
                  }
                },
                {
                  "id": "niryo_animation",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "animation": "anim1"
                  },
                  "maintenance": true
                },
                {
                  "id": "niryo_pause_animation",
                  "icon": "fa-fw fas fa-pause"
                }
              ]
            },
            {
              "id": 336,
              "card": 54,
              "name": "Animation rails stop",
              "index": 13,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_play_animation",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "animation": "reset"
                  }
                },
                {
                  "id": "waffle_factory_pause_animation",
                  "icon": "fa-fw fas fa-pause"
                }
              ]
            },
            {
              "id": 341,
              "card": 54,
              "name": "Animation rails Niryo",
              "index": 14,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_play_animation",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "animation": "niryo_init"
                  }
                },
                {
                  "id": "waffle_factory_play_animation",
                  "icon": "fa-fw fas fa-dice-two",
                  "extra": {
                    "animation": "niryo_end"
                  }
                }
              ]
            },
            {
              "id": 342,
              "card": 54,
              "name": "Animation rails gaufre 1",
              "index": 15,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_play_animation",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "animation": "first_waffle_init"
                  }
                },
                {
                  "id": "waffle_factory_play_animation",
                  "icon": "fa-fw fas fa-dice-two",
                  "extra": {
                    "animation": "waffle_end"
                  }
                }
              ]
            },
            {
              "id": 343,
              "card": 54,
              "name": "Animation rails gaufre 2",
              "index": 16,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_play_animation",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "animation": "second_waffle_init"
                  }
                }
              ]
            },
            {
              "id": 324,
              "card": 54,
              "name": "Moteurs",
              "index": 22,
              "maintenance": false,
              "widget": "waffle_factory",
              "widget_params": ""
            },
            {
              "id": 287,
              "card": 54,
              "name": "Imprimante contrôles",
              "index": 23,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "printer_homing",
                  "icon": "fa-fw fas fa-home"
                },
                {
                  "id": "waffle_factory_printer",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "resume"
                  },
                  "maintenance": true
                },
                {
                  "id": "waffle_factory_printer",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "halt"
                  },
                  "maintenance": true
                },
                {
                  "id": "waffle_factory_printer",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop"
                  },
                  "maintenance": true
                }
              ]
            },
            {
              "id": 347,
              "card": 54,
              "name": "Impression patterns",
              "index": 24,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_factory_print_pattern",
                  "icon": "fa-fw fas fa-heart",
                  "extra": {
                    "pattern": "heart"
                  }
                },
                {
                  "id": "waffle_factory_print_pattern",
                  "icon": "fa-fw fab fa-medium-m",
                  "extra": {
                    "pattern": "M"
                  }
                },
                {
                  "id": "waffle_factory_print_pattern",
                  "icon": "fa-fw fas fa-tint",
                  "extra": {
                    "pattern": "purge"
                  }
                }
              ]
            },
            {
              "id": 350,
              "card": 54,
              "name": "Code GRBL",
              "index": 27,
              "maintenance": true,
              "widget": "textarea",
              "widget_params": {
                "id": "printer_instructions"
              }
            }
          ]
        },
        {
          "id": 16,
          "name": "Salle serveur",
          "index": 10,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 83,
              "card": 16,
              "name": "Digicode",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "server_room_lock_reset",
                  "icon": "fa-fw fas fa-undo-alt"
                },
                {
                  "id": "server_room_lock_enable",
                  "icon": "fa-fw fas fa-gamepad"
                }
              ]
            },
            {
              "id": 150,
              "card": 16,
              "name": "Machine à fumée",
              "index": 1,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "fog_machine_turn_on",
                  "icon": "fa-fw fas fa-temperature-high"
                },
                {
                  "id": "fog_machine_turn_off",
                  "icon": "fa-fw fas fa-power-off"
                },
                {
                  "id": "fog_machine_send_fog",
                  "icon": "fa-fw fas fa-smog"
                }
              ]
            },
            {
              "id": 264,
              "card": 16,
              "name": "Labyrinthe",
              "index": 5,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "maze_playing",
                  "icon": "fa-fw fas fa-gamepad"
                },
                {
                  "id": "maze_alarm",
                  "icon": "fa-fw fas fa-bell"
                },
                {
                  "id": "secure_floor_calibrate",
                  "icon": "fa-fw fas fa-balance-scale"
                },
                {
                  "id": "maze_success",
                  "icon": "fa-fw fas fa-check"
                },
                {
                  "id": "maze_reset",
                  "icon": "fa-fw fas fa-undo-alt"
                }
              ]
            },
            {
              "id": 326,
              "card": 16,
              "name": "Relais",
              "index": 5,
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "alarm_relays",
                  "icon": "fa-fw fas fa-bell",
                  "extra": {
                    "activated": true
                  }
                },
                {
                  "id": "alarm_relays",
                  "icon": "fa-fw fas fa-check",
                  "extra": {
                    "activated": false
                  }
                }
              ]
            },
            {
              "id": 385,
              "card": 16,
              "name": "Fumée continue",
              "index": 6,
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "boost_fog_timer",
                "execute_help": "Envoie périodiquement de la fumée."
              }
            },
            {
              "id": 332,
              "card": 16,
              "name": "Serveur root",
              "index": 29,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "root_server_reset",
                  "icon": "fa-fw fas fa-undo-alt"
                },
                {
                  "id": "root_server_show_ui",
                  "icon": "fa-fw fas fa-gamepad"
                },
                {
                  "id": "root_server_success",
                  "icon": "fa-fw fas fa-check"
                }
              ]
            },
            {
              "id": 333,
              "card": 16,
              "name": "Animations",
              "index": 30,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "root_server_play_animation",
                  "icon": "fa-fw fas fa-beer",
                  "extra": {
                    "animation_id": "beer"
                  }
                }
              ]
            },
            {
              "id": 399,
              "card": 16,
              "name": "Root server",
              "index": 30,
              "maintenance": false,
              "widget": "root_server",
              "widget_params": ""
            },
            {
              "id": 370,
              "card": 16,
              "name": "J'ai imprimé le code de la porte",
              "index": 100,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_2",
                    "localized": true
                  },
                  "help": "Je suis détenu dans la salle serveur ! Je vous ai imprimé le code de la porte."
                }
              ]
            },
            {
              "id": 371,
              "card": 16,
              "name": "Désactiver alarme sortez",
              "index": 101,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_3",
                    "localized": true
                  },
                  "help": "Je ne peux désactiver l'alarme que si vous sortez tous de la pièce."
                }
              ]
            },
            {
              "id": 372,
              "card": 16,
              "name": "Deux modules pour désarmer",
              "index": 102,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_4",
                    "localized": true
                  },
                  "help": "Placez-vous sur les deux modules d'identification pour désarmer le système de sécurité."
                }
              ]
            },
            {
              "id": 373,
              "card": 16,
              "name": "Fonction mot de passe oublié",
              "index": 103,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_5",
                    "localized": true
                  },
                  "help": "Madame Poivre a configuré le mot de passe, seule elle le connait ! Mmmh... Je viens de voir qu'il y a une fonction mot de passe oublié."
                }
              ]
            },
            {
              "id": 374,
              "card": 16,
              "name": "Ingrédient secret disponibilité",
              "index": 104,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_6",
                    "localized": true
                  },
                  "help": "J'utilise un ingrédient secret dans toutes mes recettes, le module de disponibilité vous aidera pour le découvrir !"
                }
              ]
            },
            {
              "id": 379,
              "card": 16,
              "name": "Vite, sortez !",
              "index": 105,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "sound_id": "marmitron_7",
                    "localized": true
                  },
                  "help": "Vite, sortez ! Merci à vous et fuyez vite !"
                }
              ]
            }
          ]
        },
        {
          "id": 58,
          "name": "Global",
          "index": 12,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 313,
              "card": 58,
              "name": "Mode épileptique",
              "index": 0,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "epileptic_mode"
              }
            },
            {
              "id": 322,
              "card": 58,
              "name": "Langue",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "localize",
                  "icon": "fa-fw fas fa-frog",
                  "extra": {
                    "category": "localize",
                    "value": "fr"
                  }
                },
                {
                  "id": "localize",
                  "icon": "fa-fw fas fa-bacon",
                  "extra": {
                    "category": "localize",
                    "value": "en"
                  }
                }
              ]
            },
            {
              "id": 334,
              "card": 58,
              "name": "Niryo animation",
              "index": 2,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "niryo_animation"
              }
            },
            {
              "id": 335,
              "card": 58,
              "name": "Intro Mme Poivre",
              "index": 3,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "ms_pepper_intro"
              }
            },
            {
              "id": 337,
              "card": 58,
              "name": "Final par réfectoire",
              "index": 4,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "final_by_refectory"
              }
            },
            {
              "id": 376,
              "card": 58,
              "name": "Dry print",
              "index": 5,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "dry_print"
              }
            },
            {
              "id": 380,
              "card": 58,
              "name": "Animation Niryo et imprimante",
              "index": 6,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "order_with_niryo_and_printer"
              }
            },
            {
              "id": 375,
              "card": 58,
              "name": "Intro seulement",
              "index": 9,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_ms_pepper_here_you_are",
                  "icon": "fa-fw fas fa-play"
                }
              ]
            },
            {
              "id": 398,
              "card": 58,
              "name": "Indices auto",
              "index": 15,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "autostart_timers"
              }
            },
            {
              "id": 392,
              "card": 58,
              "name": "Trappe de service",
              "index": 20,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "backstage_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "backstage_trapdoor_close",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 393,
              "card": 58,
              "name": "Verouillage trappe de service",
              "index": 21,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "input_device",
                "key": "backstage_limit_switch"
              }
            }
          ]
        },
        {
          "id": 5,
          "name": "Musique",
          "index": 20,
          "roomIds": [1, 2],
          "rows": [
            {
              "id": 14,
              "card": 5,
              "name": "Volume master",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player_set_master_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0
                  }
                },
                {
                  "id": "music_player_set_master_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40
                  }
                },
                {
                  "id": "music_player_set_master_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70
                  }
                },
                {
                  "id": "music_player_set_master_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100
                  }
                }
              ]
            },
            {
              "id": 15,
              "card": 5,
              "name": "Track 1",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track1"
                  }
                }
              ]
            },
            {
              "id": 16,
              "card": 5,
              "name": "Track 2",
              "index": 3,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track2"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track2"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track2"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track2"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track2"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track2"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track2"
                  }
                }
              ]
            },
            {
              "id": 17,
              "card": 5,
              "name": "Track 3",
              "index": 4,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track3"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track3"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track3"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track3"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track3"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track3"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track3"
                  }
                }
              ]
            },
            {
              "id": 18,
              "card": 5,
              "name": "Track 3.5",
              "index": 5,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track35"
                  }
                }
              ]
            },
            {
              "id": 19,
              "card": 5,
              "name": "Track 4",
              "index": 6,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track4"
                  }
                }
              ]
            },
            {
              "id": 20,
              "card": 5,
              "name": "Track 5",
              "index": 7,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track5"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track5"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track5"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track5"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track5"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track5"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track5"
                  }
                }
              ]
            },
            {
              "id": 21,
              "card": 5,
              "name": "Track 6.1",
              "index": 8,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track61"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track61"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track61"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track61"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track61"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track61"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track61"
                  }
                }
              ]
            },
            {
              "id": 22,
              "card": 5,
              "name": "Track 6.2",
              "index": 9,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track62"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track62"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track62"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track62"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track62"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track62"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track62"
                  }
                }
              ]
            },
            {
              "id": 23,
              "card": 5,
              "name": "Track 6.3",
              "index": 10,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track63"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track63"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track63"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track63"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track63"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track63"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track63"
                  }
                }
              ]
            },
            {
              "id": 24,
              "card": 5,
              "name": "Track 7",
              "index": 11,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track7"
                  }
                }
              ]
            },
            {
              "id": 25,
              "card": 5,
              "name": "Track 8",
              "index": 12,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track8"
                  }
                }
              ]
            },
            {
              "id": 26,
              "card": 5,
              "name": "Track 9.1",
              "index": 13,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track91"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track91"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track91"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track91"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track91"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track91"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track91"
                  }
                }
              ]
            },
            {
              "id": 27,
              "card": 5,
              "name": "Track 9.2",
              "index": 14,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track92"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track92"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track92"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track92"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track92"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track92"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track92"
                  }
                }
              ]
            },
            {
              "id": 325,
              "card": 5,
              "name": "Track 5 glitch",
              "index": 15,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track5glitch"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track5glitch"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track5glitch"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track5glitch"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track5glitch"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track5glitch"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track5glitch"
                  }
                }
              ]
            },
            {
              "id": 344,
              "card": 5,
              "name": "Alarme",
              "index": 16,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "alarm"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "alarm"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "alarm"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "alarm"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "alarm"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "alarm"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "alarm"
                  }
                }
              ]
            },
            {
              "id": 345,
              "card": 5,
              "name": "Sons",
              "index": 17,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "play_sound",
                  "icon": "fa-fw fas fa-barcode",
                  "extra": {
                    "sound_id": "scan"
                  }
                },
                {
                  "id": "play_sound",
                  "icon": "fa-fw far fa-bell",
                  "extra": {
                    "sound_id": "laser"
                  }
                }
              ]
            }
          ]
        },
        {
          "id": 56,
          "name": "Spécifique D1",
          "index": 0,
          "roomIds": [1],
          "rows": [
            {
              "id": 328,
              "card": 59,
              "name": "Lasers",
              "index": 0,
              "maintenance": false,
              "widget": "lasers",
              "widget_params": [
                {
                  "label": "1",
                  "node": "laser_maze.a",
                  "index": 0,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "2",
                  "node": "laser_maze.a",
                  "index": 1,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "3",
                  "node": "laser_maze.a",
                  "index": 2,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "4",
                  "node": "laser_maze.a",
                  "index": 3,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "5",
                  "node": "laser_maze.a",
                  "index": 4,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "6",
                  "node": "laser_maze.a",
                  "index": 5,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "7",
                  "node": "laser_maze.a",
                  "index": 6,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "8",
                  "node": "laser_maze.a",
                  "index": 7,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "9",
                  "node": "laser_maze.a",
                  "index": 8,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "10",
                  "node": "laser_maze.a",
                  "index": 9,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "11",
                  "node": "laser_maze.a",
                  "index": 10,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "12",
                  "node": "laser_maze.a",
                  "index": 11,
                  "easy": false,
                  "normal": false,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "13",
                  "node": "laser_maze.a",
                  "index": 12,
                  "easy": true,
                  "normal": false,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "14",
                  "node": "laser_maze.a",
                  "index": 13,
                  "easy": false,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "15",
                  "node": "laser_maze.a",
                  "index": 14,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "16",
                  "node": "laser_maze.b",
                  "index": 0,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "17",
                  "node": "laser_maze.b",
                  "index": 1,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "18",
                  "node": "laser_maze.b",
                  "index": 2,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "19",
                  "node": "laser_maze.b",
                  "index": 3,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "20",
                  "node": "laser_maze.b",
                  "index": 4,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "21",
                  "node": "laser_maze.b",
                  "index": 5,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "22",
                  "node": "laser_maze.b",
                  "index": 6,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "B"
                }
              ]
            },
            {
              "id": 394,
              "card": 59,
              "name": "Verouillage trappe Niryo",
              "index": 1,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "input_device",
                "key": "niryo_backstage_limit_switch"
              }
            },
            {
              "id": 396,
              "card": 59,
              "name": "Trappe de service Niryo",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "niryo_backstage_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "niryo_backstage_trapdoor_close",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 378,
              "card": 59,
              "name": "Registre",
              "index": 2,
              "maintenance": false,
              "widget": "node_register",
              "widget_params": {
                "nodes": [
                  {
                    "name": "chopsticks"
                  },
                  {
                    "name": "control_panel"
                  },
                  {
                    "name": "holographic_menu"
                  },
                  {
                    "name": "load_cells"
                  },
                  {
                    "name": "advertiser"
                  },
                  {
                    "name": "street_display"
                  },
                  {
                    "name": "ventilation_panel"
                  },
                  {
                    "name": "payment_module"
                  },
                  {
                    "name": "vents_locker"
                  },
                  {
                    "name": "refectory_lights"
                  },
                  {
                    "name": "street_lights"
                  },
                  {
                    "name": "front_door_magnet"
                  },
                  {
                    "name": "orders"
                  },
                  {
                    "name": "synchronizer"
                  },
                  {
                    "name": "root_server"
                  },
                  {
                    "name": "inventory"
                  },
                  {
                    "name": "digital_lock"
                  },
                  {
                    "name": "sokoban_controls"
                  },
                  {
                    "name": "emergency_exit"
                  },
                  {
                    "name": "stock_lights"
                  },
                  {
                    "name": "cylinders"
                  },
                  {
                    "name": "secure_floor"
                  },
                  {
                    "name": "fog_machine"
                  },
                  {
                    "name": "niryo"
                  },
                  {
                    "name": "laser_maze_a"
                  },
                  {
                    "name": "laser_maze_b"
                  },
                  {
                    "name": "relays"
                  },
                  {
                    "name": "human_authenticator"
                  },
                  {
                    "name": "waffle_factory"
                  },
                  {
                    "name": "waffle_trapdoor"
                  },
                  {
                    "name": "waffle_limit_switch"
                  },
                  {
                    "name": "digital_lock_shutdown"
                  },
                  {
                    "name": "music_player"
                  },
                  {
                    "name": "sound_player"
                  },
                  {
                    "name": "backstage_trapdoor"
                  },
                  {
                    "name": "backstage_limit_switch"
                  },
                  {
                    "name": "niryo_backstage_trapdoor"
                  },
                  {
                    "name": "niryo_backstage_limit_switch"
                  },
                  {
                    "name": "d2_c1_shutdown"
                  },
                  {
                    "name": "d2_c2_shutdown"
                  },
                  {
                    "name": "d2_c3_shutdown"
                  }
                ]
              }
            }
          ]
        },
        {
          "id": 59,
          "name": "Spécifique D2",
          "index": 0,
          "roomIds": [2],
          "rows": [
            {
              "id": 328,
              "card": 59,
              "name": "Lasers",
              "index": 0,
              "maintenance": false,
              "widget": "lasers",
              "widget_params": [
                {
                  "label": "1",
                  "node": "laser_maze.a",
                  "index": 0,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "2",
                  "node": "laser_maze.a",
                  "index": 1,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "3",
                  "node": "laser_maze.a",
                  "index": 2,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "4",
                  "node": "laser_maze.a",
                  "index": 3,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "5",
                  "node": "laser_maze.a",
                  "index": 4,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "6",
                  "node": "laser_maze.a",
                  "index": 5,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": true,
                  "prefix": "A"
                },
                {
                  "label": "7",
                  "node": "laser_maze.a",
                  "index": 6,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "8",
                  "node": "laser_maze.a",
                  "index": 7,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "9",
                  "node": "laser_maze.a",
                  "index": 8,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "10",
                  "node": "laser_maze.a",
                  "index": 9,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "11",
                  "node": "laser_maze.a",
                  "index": 10,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "12",
                  "node": "laser_maze.a",
                  "index": 11,
                  "easy": false,
                  "normal": false,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "13",
                  "node": "laser_maze.a",
                  "index": 12,
                  "easy": true,
                  "normal": false,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "14",
                  "node": "laser_maze.a",
                  "index": 13,
                  "easy": false,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "15",
                  "node": "laser_maze.a",
                  "index": 14,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "A"
                },
                {
                  "label": "16",
                  "node": "laser_maze.b",
                  "index": 0,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "17",
                  "node": "laser_maze.b",
                  "index": 1,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "18",
                  "node": "laser_maze.b",
                  "index": 2,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "19",
                  "node": "laser_maze.b",
                  "index": 3,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "20",
                  "node": "laser_maze.b",
                  "index": 4,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "21",
                  "node": "laser_maze.b",
                  "index": 5,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": true,
                  "dynamic": false,
                  "prefix": "B"
                },
                {
                  "label": "22",
                  "node": "laser_maze.b",
                  "index": 6,
                  "easy": true,
                  "normal": true,
                  "hard": true,
                  "wall": false,
                  "dynamic": false,
                  "prefix": "B"
                }
              ]
            },
            {
              "id": 394,
              "card": 59,
              "name": "Verouillage trappe Niryo",
              "index": 1,
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "input_device",
                "key": "niryo_backstage_limit_switch"
              }
            },
            {
              "id": 396,
              "card": 59,
              "name": "Trappe de service Niryo",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "niryo_backstage_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "niryo_backstage_trapdoor_close",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 378,
              "card": 59,
              "name": "Registre",
              "index": 2,
              "maintenance": false,
              "widget": "node_register",
              "widget_params": {
                "nodes": [
                  {
                    "name": "chopsticks"
                  },
                  {
                    "name": "control_panel"
                  },
                  {
                    "name": "holographic_menu"
                  },
                  {
                    "name": "load_cells"
                  },
                  {
                    "name": "advertiser"
                  },
                  {
                    "name": "street_display"
                  },
                  {
                    "name": "ventilation_panel"
                  },
                  {
                    "name": "payment_module"
                  },
                  {
                    "name": "vents_locker"
                  },
                  {
                    "name": "refectory_lights"
                  },
                  {
                    "name": "street_lights"
                  },
                  {
                    "name": "front_door_magnet"
                  },
                  {
                    "name": "orders"
                  },
                  {
                    "name": "synchronizer"
                  },
                  {
                    "name": "root_server"
                  },
                  {
                    "name": "inventory"
                  },
                  {
                    "name": "digital_lock"
                  },
                  {
                    "name": "sokoban_controls"
                  },
                  {
                    "name": "emergency_exit"
                  },
                  {
                    "name": "stock_lights"
                  },
                  {
                    "name": "cylinders"
                  },
                  {
                    "name": "secure_floor"
                  },
                  {
                    "name": "fog_machine"
                  },
                  {
                    "name": "niryo"
                  },
                  {
                    "name": "laser_maze_a"
                  },
                  {
                    "name": "laser_maze_b"
                  },
                  {
                    "name": "relays"
                  },
                  {
                    "name": "human_authenticator"
                  },
                  {
                    "name": "waffle_factory"
                  },
                  {
                    "name": "waffle_trapdoor"
                  },
                  {
                    "name": "waffle_limit_switch"
                  },
                  {
                    "name": "digital_lock_shutdown"
                  },
                  {
                    "name": "music_player"
                  },
                  {
                    "name": "sound_player"
                  },
                  {
                    "name": "backstage_trapdoor"
                  },
                  {
                    "name": "backstage_limit_switch"
                  },
                  {
                    "name": "niryo_backstage_trapdoor"
                  },
                  {
                    "name": "niryo_backstage_limit_switch"
                  },
                  {
                    "name": "d2_c1_shutdown"
                  },
                  {
                    "name": "d2_c2_shutdown"
                  },
                  {
                    "name": "d2_c3_shutdown"
                  }
                ]
              }
            }
          ]
        },
        {
          "id": 57,
          "name": "Casiers",
          "index": 0,
          "roomIds": [3],
          "rows": [
            {
              "id": 308,
              "card": 57,
              "name": "Ouverture (1/3)",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "category": "unlock",
                    "locker_index": 0,
                    "channel": "justescape.player_lockers"
                  }
                },
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-dice-two",
                  "extra": {
                    "category": "unlock",
                    "locker_index": 1,
                    "channel": "justescape.player_lockers"
                  }
                },
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-dice-three",
                  "extra": {
                    "category": "unlock",
                    "locker_index": 2,
                    "channel": "justescape.player_lockers"
                  }
                }
              ]
            },
            {
              "id": 309,
              "card": 57,
              "name": "Ouverture (2/3)",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-dice-four",
                  "extra": {
                    "category": "unlock",
                    "locker_index": 3,
                    "channel": "justescape.player_lockers"
                  }
                },
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-dice-five",
                  "extra": {
                    "category": "unlock",
                    "locker_index": 4,
                    "channel": "justescape.player_lockers"
                  }
                },
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-dice-six",
                  "extra": {
                    "category": "unlock",
                    "locker_index": 5,
                    "channel": "justescape.player_lockers"
                  }
                }
              ]
            },
            {
              "id": 310,
              "card": 57,
              "name": "Ouverture (3/3)",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "player_lockers_open",
                  "icon": "fa-fw fas fa-unlock",
                  "extra": {
                    "category": "unlock_from_bitmask",
                    "bitmask": 63,
                    "channel": "justescape.player_lockers"
                  }
                }
              ]
            }
          ]
        },
        {
          "id": 60,
          "name": "Shutdown",
          "index": 1,
          "roomIds": [3],
          "rows": [
            {
              "id": 330,
              "card": 60,
              "name": "D1",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "d1_poweroff",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "category": "shutdown",
                    "channel": "d1.broadcast"
                  }
                }
              ]
            },
            {
              "id": 331,
              "card": 60,
              "name": "D2",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "d2_poweroff",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "category": "shutdown",
                    "channel": "d2.broadcast"
                  }
                }
              ]
            }
          ]
        },
        {
          "id": 61,
          "name": "Escape the Boom",
          "index": 2,
          "roomIds": [3],
          "rows": [
            {
              "id": 410,
              "card": 61,
              "name": "Porte réfectoire",
              "index": 0,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "front_door_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "front_door_close",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 411,
              "card": 61,
              "name": "Porte de secours",
              "index": 1,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "emergency_exit_unlock_to_outside",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "emergency_exit_lock_to_outside",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 412,
              "card": 61,
              "name": "Porte stock<->salle serveurs",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "emergency_exit_unlock_stock_to_machine",
                  "icon": "fa-fw fas fa-lock-open"
                },
                {
                  "id": "emergency_exit_lock_stock_to_machine",
                  "icon": "fa-fw fas fa-lock"
                }
              ]
            },
            {
              "id": 429,
              "card": 61,
              "name": "Conduit d'aération",
              "index": 2,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "vents_locker",
                  "icon": "fa-fw fas fa-lock-open",
                  "extra": {
                    "lock": false
                  }
                },
                {
                  "id": "vents_locker",
                  "icon": "fa-fw fas fa-lock",
                  "extra": {
                    "lock": true
                  }
                }
              ]
            },
            {
              "id": 413,
              "card": 61,
              "name": "Blanc réfectoire",
              "index": 3,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "white"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "white"
                  }
                }
              ]
            },
            {
              "id": 414,
              "card": 61,
              "name": "Bleu réfectoire",
              "index": 4,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "blue"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "blue"
                  }
                }
              ]
            },
            {
              "id": 415,
              "card": 61,
              "name": "Orange réfectoire",
              "index": 5,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "orange"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "orange"
                  }
                }
              ]
            },
            {
              "id": 416,
              "card": 61,
              "name": "Vert réfectoire",
              "index": 6,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "green"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "green"
                  }
                }
              ]
            },
            {
              "id": 417,
              "card": 61,
              "name": "Rouge réfectoire",
              "index": 6,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "red"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "red"
                  }
                }
              ]
            },
            {
              "id": 418,
              "card": 61,
              "name": "Rose réfectoire",
              "index": 7,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw far fa-sun",
                  "extra": {
                    "on": true,
                    "color": "pink"
                  }
                },
                {
                  "id": "refectory_lights",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "on": false,
                    "color": "pink"
                  }
                }
              ]
            },
            {
              "id": 419,
              "card": 61,
              "name": "Lumière stock",
              "index": 8,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "stock_lights_high",
                  "icon": "fa-fw far fa-sun"
                },
                {
                  "id": "stock_lights_low",
                  "icon": "fa-fw far fa-moon"
                },
                {
                  "id": "stock_lights_off",
                  "icon": "fa-fw fas fa-power-off"
                }
              ]
            },
            {
              "id": 430,
              "card": 61,
              "name": "Lumière salle serveurs",
              "index": 8,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "set_secure_floor_all_leds_color",
                  "icon": "fa-fw fas fa-sun",
                  "extra": {
                    "color": "white"
                  }
                },
                {
                  "id": "set_secure_floor_all_leds_color",
                  "icon": "fa-fw fas fa-carrot",
                  "extra": {
                    "color": "orange"
                  }
                },
                {
                  "id": "set_secure_floor_all_leds_color",
                  "icon": "fa-fw fas fa-pizza-slice",
                  "extra": {
                    "color": "red"
                  }
                },
                {
                  "id": "set_secure_floor_all_leds_color",
                  "icon": "fa-fw fas fa-power-off",
                  "extra": {
                    "color": "black"
                  }
                }
              ]
            },
            {
              "id": 420,
              "card": 61,
              "name": "Track 1",
              "index": 9,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track1"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track1"
                  }
                }
              ]
            },
            {
              "id": 421,
              "card": 61,
              "name": "Track 3.5",
              "index": 10,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track35"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track35"
                  }
                }
              ]
            },
            {
              "id": 422,
              "card": 61,
              "name": "Track 4",
              "index": 11,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track4"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track4"
                  }
                }
              ]
            },
            {
              "id": 423,
              "card": 61,
              "name": "Track 7",
              "index": 12,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track7"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track7"
                  }
                }
              ]
            },
            {
              "id": 424,
              "card": 61,
              "name": "Track 8",
              "index": 13,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-play",
                  "extra": {
                    "action": "play",
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-pause",
                  "extra": {
                    "action": "pause",
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player",
                  "icon": "fa-fw fas fa-undo-alt",
                  "extra": {
                    "action": "stop",
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-mute",
                  "extra": {
                    "volume": 0,
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-off",
                  "extra": {
                    "volume": 40,
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-down",
                  "extra": {
                    "volume": 70,
                    "track_id": "track8"
                  }
                },
                {
                  "id": "music_player_set_volume",
                  "icon": "fa-fw fas fa-volume-up",
                  "extra": {
                    "volume": 100,
                    "track_id": "track8"
                  }
                }
              ]
            },
            {
              "id": 426,
              "card": 61,
              "name": "Chauffe machine à fumée",
              "index": 14,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "fog_machine_turn_on",
                  "icon": "fa-fw fas fa-temperature-high"
                }
              ]
            },
            {
              "id": 427,
              "card": 61,
              "name": "Stop chauffe machine à fumée",
              "index": 15,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "fog_machine_turn_off",
                  "icon": "fa-fw fas fa-power-off"
                }
              ]
            },
            {
              "id": 428,
              "card": 61,
              "name": "Envoyer de la fumée",
              "index": 15,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "fog_machine_send_fog",
                  "icon": "fa-fw fas fa-smog"
                }
              ]
            },
            {
              "id": 425,
              "card": 61,
              "name": "Animation chambres stock",
              "index": 16,
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-one",
                  "extra": {
                    "id": "potjevleesch"
                  }
                },
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-two",
                  "extra": {
                    "id": "salade_flamande"
                  }
                },
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-three",
                  "extra": {
                    "id": "cambraisienne"
                  }
                },
                {
                  "id": "check_cylinders_availability",
                  "icon": "fa-fw fas fa-dice-four",
                  "extra": {
                    "id": "gaufresque"
                  }
                }
              ]
            }
          ]
        }
      ],
      selected: null,
    }
  },
  watch: {
    selected(newValue) {
      roomStore.commit(
        'setRoomDefaultPublicationChannel',
        {roomId: this.roomId, defaultPublicationChannel: newValue}
      )
    },
  },
  created() {
    for (var room of roomStore.state.rooms) {
      if (room.id == this.roomId) {
        this.selected = room.default_publication_channel
      }
    }
  },
  props: ['roomId']
}
</script>
