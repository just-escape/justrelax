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
          v-for="(card, cardIndex) in cards.filter(card => card.roomIds.includes(roomId))"
          :key="cardIndex"
          class="col-12 col-lg-6 col-xl-3 mb-1 px-1"
        >
          <ActionCard
            :roomId="roomId"
            :card="card"
            :cardId="cardIndex"
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
          "name": "Contrôle",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Baguettes",
              "maintenance": false,
              "widget": "chopsticks",
              "widget_params": ""
            },
            {
              "name": "Status",
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
              "name": "Table",
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
              "name": "Force manual mode",
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
              "name": "Rappel CONTROL",
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "chopsticks_voice_clue_1",
                "execute_help": "Je vous rappelle que vous devez acceder au pannel de controle pour désactiver le marmitron."
              }
            },
            {
              "name": "Tige pour CONTROL",
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "chopsticks_voice_clue_2",
                "execute_help": "Le logiciel de maintenance indique que vous avez besoin d'une tige pour enclencher les mécanismes du panel de contrôle."
              }
            },
            {
              "name": "Configurez lumières",
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
              "name": "Passez en mode manuel",
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
              "name": "Panel de contrôle",
              "maintenance": false,
              "widget": "control_panel",
              "widget_params": ""
            }
          ]
        },
        {
          "name": "Lumières",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Blanc",
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
              "name": "Bleu",
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
              "name": "Orange",
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
              "name": "Vert",
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
              "name": "Rouge",
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
              "name": "Rose",
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
              "name": "Calibration dalles",
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
              "name": "Lumières désactivées",
              "maintenance": false,
              "widget": "synchronizer_lights",
              "widget_params": ""
            }
          ]
        },
        {
          "name": "Écran synchro",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Status",
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
              "name": "Synchronizer",
              "maintenance": false,
              "widget": "synchronizer",
              "widget_params": ""
            },
            {
              "name": "Overlay vidéo",
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
              "name": "Menu : slide",
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
              "name": "Menu : X",
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
              "name": "Menu : Y",
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
              "name": "Menu : error",
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
              "name": "Succès forcé",
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
              "name": "Log lumières",
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
              "name": "Log menu",
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
              "name": "Indications utiles à lire",
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
              "name": "Retrouvez les plats/prix",
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
              "name": "Emballages dans la poubelle",
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
              "name": "Il reste des tickets de caisse",
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
              "name": "Aidez-vous des pubs",
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
              "name": "Regardez sous vos pieds",
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
              "name": "Concentrez-vous sur 1 lumière",
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
          "name": "Rue / publicités",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Vidéo Marmitron",
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
              "name": "Vidéo publicité glitchée",
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
              "name": "Vidéo pub gaufresque",
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
              "name": "Vidéo pubs",
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
              "name": "Vidéo Mme Poivre",
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
              "name": "Interface menu",
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
              "name": "Porte",
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "front_door_open",
                  "icon": "fa-fw fas fa-lock-open",
                  "extra": {
                    "with_sound": true
                  }
                },
                {
                  "id": "front_door_open",
                  "icon": "fa-fw fas fa-volume-mute"
                },
              ]
            },
            {
              "name": "Lumières rue",
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
          "name": "Écran commandes",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Status",
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
              "name": "Module de paiement",
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
              "name": "Instruction doc ventil",
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
              "name": "Transférez néofrancs bague",
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
              "name": "Commande hauteur moyen",
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
          "name": "Ventilation",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Ignorer le panel de ventilation",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "ventilation_panel_skip"
              }
            },
            {
              "name": "Timer ignorer le panel",
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "ventilation_panel_skip_timer",
                "execute_help": "Ignore automatiquement le panel de ventilation."
              }
            },
            {
              "name": "Conduit",
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
              "name": "Module de ventilation",
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
              "name": "Plus vite plus loin",
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
              "name": "Ventilation",
              "maintenance": false,
              "widget": "ventilation_panel",
              "widget_params": ""
            }
          ]
        },
        {
          "name": "Stock",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Lumières",
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
              "name": "Porte vers l'extérieur",
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
              "name": "Porte stock<->salle serveurs",
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "emergency_exit_unlock_stock_to_machine",
                  "icon": "fa-fw fas fa-lock-open",
                  "extra": {
                    "with_sound": true
                  }
                },
                {
                  "id": "emergency_exit_unlock_stock_to_machine",
                  "icon": "fa-fw fas fa-volume-mute"
                }
              ]
            },
            {
              "name": "Cylindres",
              "maintenance": false,
              "widget": "cylinders",
              "widget_params": ""
            },
            {
              "name": "Cylindres check",
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
              "name": "Enclenchement rotation",
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
              "name": "Rdv dans le réfectoire",
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
          "name": "Sokoban",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Reset (énigme entière)",
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
              "name": "Contrôles (1/2)",
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
              "name": "Contrôles (2/2)",
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
              "name": "Log inventaire",
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
              "name": "Déplacez-vous deuxième niveau",
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
              "name": "Logiciel aide orga virtuelle",
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
              "name": "Sokoban",
              "maintenance": false,
              "widget": "sokoban",
              "widget_params": ""
            }
          ]
        },
        {
          "name": "Usine à gaufres",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Lumière Niryo",
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
              "name": "Lumière imprimante",
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
              "name": "Trappe",
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "waffle_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                }
              ]
            },
            {
              "name": "Verouillage trappe",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "input_device",
                "key": "waffle_limit_switch"
              }
            },
            {
              "name": "Four",
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
              "name": "Niryo aimant",
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
              "name": "Niryo animations",
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
              "name": "Animation rails stop",
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
              "name": "Animation rails Niryo",
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
              "name": "Animation rails gaufre 1",
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
              "name": "Animation rails gaufre 2",
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
              "name": "Moteurs",
              "maintenance": false,
              "widget": "waffle_factory",
              "widget_params": ""
            },
            {
              "name": "Imprimante contrôles",
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
              "name": "Impression patterns",
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
              "name": "Code GRBL",
              "maintenance": true,
              "widget": "textarea",
              "widget_params": {
                "id": "printer_instructions"
              }
            }
          ]
        },
        {
          "name": "Salle serveur",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Digicode",
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
              "name": "Machine à fumée",
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
              "name": "Labyrinthe",
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
              "name": "Relais",
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
              "name": "Fumée continue",
              "maintenance": false,
              "widget": "timer",
              "widget_params": {
                "name": "boost_fog_timer",
                "execute_help": "Envoie périodiquement de la fumée."
              }
            },
            {
              "name": "Serveur root",
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
              "name": "Animations",
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
              "name": "Root server",
              "maintenance": false,
              "widget": "root_server",
              "widget_params": ""
            },
            {
              "name": "J'ai imprimé le code de la porte",
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
              "name": "Désactiver alarme sortez",
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
              "name": "Deux modules pour désarmer",
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
              "name": "Fonction mot de passe oublié",
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
              "name": "Ingrédient secret disponibilité",
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
              "name": "Vite, sortez !",
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
          "name": "Global",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Mode épileptique",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "epileptic_mode"
              }
            },
            {
              "name": "Langue",
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
              "name": "Curseur écrans tactiles",
              "maintenance": true,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "set_cursor_visibility",
                  "icon": "fa-fw fas fa-mouse-pointer",
                  "extra": {
                    "show": true
                  }
                },
                {
                  "id": "set_cursor_visibility",
                  "icon": "fa-fw fas fa-ban",
                  "extra": {
                    "show": false
                  }
                }
              ]
            },
            {
              "name": "Niryo animation",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "niryo_animation"
              }
            },
            {
              "name": "Intro Mme Poivre",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "ms_pepper_intro"
              }
            },
            {
              "name": "Final par réfectoire",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "final_by_refectory"
              }
            },
            {
              "name": "Dry print",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "dry_print"
              }
            },
            {
              "name": "Animation Niryo et imprimante",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "order_with_niryo_and_printer"
              }
            },
            {
              "name": "Intro seulement",
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
              "name": "Indices auto",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "checkbox",
                "key": "autostart_timers"
              }
            },
            {
              "name": "Trappe de service",
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "backstage_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
              ]
            },
            {
              "name": "Verouillage trappe de service",
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
          "name": "Musique",
          "roomIds": [1, 2],
          "rows": [
            {
              "name": "Volume master",
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
              "name": "Track 1",
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
              "name": "Track 2",
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
              "name": "Track 3",
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
              "name": "Track 3.5",
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
              "name": "Track 4",
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
              "name": "Track 5",
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
              "name": "Track 6.1",
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
              "name": "Track 6.2",
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
              "name": "Track 6.3",
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
              "name": "Track 7",
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
              "name": "Track 8",
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
              "name": "Track 9.1",
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
              "name": "Track 9.2",
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
              "name": "Track 5 glitch",
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
              "name": "Alarme",
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
            }
          ]
        },
        {
          "name": "Spécifique D1",
          "roomIds": [1],
          "rows": [
            {
              "name": "Lasers",
              "maintenance": false,
              "widget": "lasers",
              "widget_params": {
                expected_prefixes: ['A'],
                map: [
                  {
                    "label": "1",
                    "node": "laser_maze",
                    "index": 0,
                    "easy": false,
                    "normal": false,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "2",
                    "node": "laser_maze",
                    "index": 1,
                    "easy": false,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "3",
                    "node": "laser_maze",
                    "index": 2,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "4",
                    "node": "laser_maze",
                    "index": 3,
                    "easy": false,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "5",
                    "node": "laser_maze",
                    "index": 4,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "6",
                    "node": "laser_maze",
                    "index": 5,
                    "easy": false,
                    "normal": false,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "7",
                    "node": "laser_maze",
                    "index": 6,
                    "easy": false,
                    "normal": false,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "8",
                    "node": "laser_maze",
                    "index": 7,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "9",
                    "node": "laser_maze",
                    "index": 8,
                    "easy": false,
                    "normal": false,
                    "hard": true,
                    "wall": false,
                    "dynamic": false,
                    "prefix": "A"
                  },
                  {
                    "label": "10",
                    "node": "laser_maze",
                    "index": 9,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": true,
                    "prefix": "A"
                  },
                  {
                    "label": "11",
                    "node": "laser_maze",
                    "index": 10,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": true,
                    "prefix": "A"
                  },
                  {
                    "label": "12",
                    "node": "laser_maze",
                    "index": 11,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": true,
                    "prefix": "A"
                  },
                  {
                    "label": "13",
                    "node": "laser_maze",
                    "index": 12,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": true,
                    "prefix": "A"
                  },
                  {
                    "label": "14",
                    "node": "laser_maze",
                    "index": 13,
                    "easy": true,
                    "normal": true,
                    "hard": true,
                    "wall": false,
                    "dynamic": true,
                    "prefix": "A"
                  }
                ]
              }
            },
            {
              "name": "Registre",
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
                    "name": "laser_maze"
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
                    "name": "d1_c1_shutdown"
                  },
                  {
                    "name": "d1_c2_shutdown"
                  },
                  {
                    "name": "d1_c3_shutdown"
                  }
                ]
              }
            }
          ]
        },
        {
          "name": "Spécifique D2",
          "roomIds": [2],
          "rows": [
            {
              "name": "Lasers",
              "maintenance": false,
              "widget": "lasers",
              "widget_params": {
                expected_prefixes: ['A', 'B'],
                map: [
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
                ],
              }
            },
            {
              "name": "Verouillage trappe Niryo",
              "maintenance": false,
              "widget": "session_data",
              "widget_params": {
                "widget": "input_device",
                "key": "niryo_backstage_limit_switch"
              }
            },
            {
              "name": "Trappe de service Niryo",
              "maintenance": false,
              "widget": "buttons_group",
              "widget_params": [
                {
                  "id": "niryo_backstage_trapdoor_open",
                  "icon": "fa-fw fas fa-lock-open"
                },
              ]
            },
            {
              "name": "Registre",
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
          "name": "Casiers",
          "roomIds": [3],
          "rows": [
            {
              "name": "Ouverture (1/3)",
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
              "name": "Ouverture (2/3)",
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
              "name": "Ouverture (3/3)",
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
          "name": "Shutdown",
          "roomIds": [3],
          "rows": [
            {
              "name": "D1",
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
              "name": "D2",
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
          "name": "Escape the Boom",
          "roomIds": [3],
          "rows": [
            {
              "name": "Porte réfectoire",
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
              "name": "Porte de secours",
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
              "name": "Porte stock<->salle serveurs",
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
              "name": "Conduit d'aération",
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
              "name": "Blanc réfectoire",
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
              "name": "Bleu réfectoire",
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
              "name": "Orange réfectoire",
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
              "name": "Vert réfectoire",
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
              "name": "Rouge réfectoire",
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
              "name": "Rose réfectoire",
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
              "name": "Lumière stock",
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
              "name": "Lumière salle serveurs",
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
              "name": "Track 1",
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
              "name": "Track 3.5",
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
              "name": "Track 4",
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
              "name": "Track 7",
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
              "name": "Track 8",
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
              "name": "Chauffe machine à fumée",
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
              "name": "Stop chauffe machine à fumée",
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
              "name": "Envoyer de la fumée",
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
              "name": "Animation chambres stock",
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
