<template>
  <div class="d-flex flex-column">
    <div v-for="motor in niryoMotors" :key="motor.id" class="d-flex flex-column mb-2">
        <div class="d-flex justify-content-between align-items-center mb-1">
            <div class="text-one-line-ellipsis min-width-100px">{{ motor.name }}</div>

            <b-button-group>
            <ButtonJaffa
                size="sm"
                :disabled="parseInt(motor.stepDelay) > parseInt(motor.liminaryStepDelay) && parseInt(motor.nLiminarySteps) > 0"
                @click="() => motorMove(motor.channel, 'motor_forward', motor.id, parseInt(motor.nSteps), parseInt(motor.stepDelay), parseInt(motor.nLiminarySteps), parseInt(motor.liminaryStepDelay))"
            >
                <i :class="'fa-fw fas fa-angle-double-left'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                :disabled="parseInt(motor.stepDelay) > parseInt(motor.liminaryStepDelay) && parseInt(motor.nLiminarySteps) > 0"
                @click="() => motorMove(motor.channel, 'motor_homing', motor.id, parseInt(motor.nSteps), parseInt(motor.stepDelay), parseInt(motor.nLiminarySteps), parseInt(motor.liminaryStepDelay))"
            >
                <i :class="'fa-fw fas fa-home'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                :disabled="parseInt(motor.stepDelay) > parseInt(motor.liminaryStepDelay) && parseInt(motor.nLiminarySteps) > 0"
                @click="() => motorMove(motor.channel, 'motor_backward', motor.id, parseInt(motor.nSteps), parseInt(motor.stepDelay), parseInt(motor.nLiminarySteps), parseInt(motor.liminaryStepDelay))"
            >
                <i :class="'fa-fw fas fa-angle-double-right'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                @click="() => motorStop(motor.channel, motor.id)"
            >
                <i :class="'fa-fw fas fa-pause'"></i>
            </ButtonJaffa>
            </b-button-group>
        </div>
        <div class="d-flex mb-1">
          <b-input class="w-25" v-model="motor.nSteps" placeholder="Steps" type="number" min="0" max="20000"></b-input>
          <b-input class="w-25" v-model="motor.stepDelay" placeholder="Délais inter-step (µs)" type="number" min="200" max="20000"></b-input>
          <b-input class="w-25" v-model="motor.nLiminarySteps" placeholder="Steps liminaires" type="number" min="0" max="20000"></b-input>
          <b-input class="w-25" v-model="motor.liminaryStepDelay" placeholder="Délais initial (µs)" type="number" min="200" max="20000"></b-input>
        </div>
    </div>

    <div v-for="dxl in niryoDynamixels" :key="dxl.id">
        <div class="text-one-line-ellipsis min-width-100px">{{ dxl.name }}</div>

        <div class="d-flex mb-1 w-100">
            <b-button-group class="mr-4">
            <ButtonJaffa
                size="sm"
                @click="() => dxlAction('dxl_torque_on', dxl.id)"
            >
                <i :class="'fa-fw far fa-sun'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                @click="() => dxlAction('dxl_torque_off', dxl.id)"
            >
                <i :class="'fa-fw fas fa-power-off'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                @click="() => dxlAction('dxl_reboot', dxl.id)"
            >
                <i :class="'fa-fw fas fa-undo-alt'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                @click="() => dxlAction('dxl_get_position', dxl.id)"
            >
                <i :class="'fa-fw fas fa-map-marker-alt'"></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                :disabled="!Number.isInteger(parseInt(dxl.position))"
                @click="() => dxlMove(dxl.id, parseInt(dxl.position))"
            >
                <i :class="'fa-fw fas fa-play'"></i>
            </ButtonJaffa>
            </b-button-group>
            <b-input class="max-width-100px" v-model="dxl.position" placeholder="Position" type="number" min="0" max="4095"></b-input>
        </div>
    </div>
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetWaffleFactory",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      niryoDynamixels: [
        {
          name: "Niryo servo radius",
          id: "radius",
          position: undefined,
        },
        {
          name: "Niryo servo poignet",
          id: "wrist",
          position: undefined,
        },
        {
          name: "Niryo servo pouce",
          id: "thumb",
          position: undefined,
        },
      ],
    }
  },
  computed: {
    niryoMotors() {
      let motors = [
        {
          name: "Convoyeur Niryo",
          id: "niryo",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Convoyeur Imprimante",
          id: "printer",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Tirette extraction",
          id: "extractor",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Tirette recharge",
          id: "reloader",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Convoyeur court",
          id: "short_one",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
      ]

      if (this.defaultChannel === 'd1.scenario') {
        // Hack, should be in widget params in the database, but it is so specific that... I got lazy
        motors = [
          ...motors,
          {
            name: "Tirette podium (d1)",
            id: "podium",
            channel: 'waffle_factory',
            nSteps: 100,
            stepDelay: 2000,
            nLiminarySteps: 0,
            liminaryStepDelay: 3000,
          },
        ]
      }

      motors = [
        ...motors,
        {
          name: "Tirette de fin",
          id: "finisher",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Niryo moteur épaule",
          id: "shoulder",
          channel: 'niryo',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Niryo moteur bras",
          id: "arm",
          channel: 'niryo',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
        {
          name: "Niryo moteur coude",
          id: "elbow",
          channel: 'niryo',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
        },
      ]

      return motors
    }
  },
  methods: {
    motorMove(motorChannel, action, motorId, nSteps, stepDelay, nLiminarySteps, liminaryStepDelay) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          motor_channel: motorChannel,
          action: action,
          motor_id: motorId,
          n_pulses: nSteps,
          step_delay: stepDelay,
          liminary_n_pulses: nLiminarySteps,
          liminary_step_delay: liminaryStepDelay,
        }
      )
    },
    motorStop(motorChannel, motorId) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          motor_channel: motorChannel,
          action: "motor_stop",
          motor_id: motorId,
        }
      )
    },
    dxlAction(action, dxlId) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          action: action,
          dxl_id: dxlId,
        }
      )
    },
    dxlMove(dxlId, position) {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          action: "dxl_move",
          dxl_id: dxlId,
          position: position,
        }
      )
    },
  },
  props: [
    "defaultChannel",
    "row",
  ]
}
</script>

<style scoped>
.max-width-100px {
  max-width: 100px;
}
</style>