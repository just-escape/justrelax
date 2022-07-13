<template>
  <div class="d-flex flex-column">
    <div class="border-deepdark rounded p-3 d-flex flex-column mb-2">
      <div class="d-flex flex-row justify-content-between align-items-center rows-striped">
        <div>Homing lancé ?</div>
        <div v-if="hasHomingBeenRun">
          <i class="fa fa-fw fa-check text-jaffa"></i>
        </div>
        <div v-else>
          <ButtonJaffa
              size="sm"
              class="position-relative"
              @click="runHomingAndPurge"
          >
              <i class="fa-fw fa fa-home"></i>
              <i
                class="fa-fw fas fa-tint position-absolute"
                style="scale: 0.7; bottom: 0; right: 0"
              ></i>
          </ButtonJaffa>
          <i class="fa fa-fw fa-times text-danger"></i>
        </div>
      </div>
      <div class="d-flex flex-row justify-content-between align-items-center rows-striped">
        <div>Printer current action</div>
        <div>{{ printerCurrentAction == null ? 'IDLE' : printerCurrentAction }}</div>
      </div>
      <div class="d-flex flex-row justify-content-between align-items-center rows-striped">
        <div>Moteurs gaufre</div>
        <div v-if="!motorsErrorMode">
          <i class="fa fa-fw fa-check text-jaffa"></i>
        </div>
        <div v-else>
            <ButtonJaffa
                size="sm"
                @click="ackMotorsError"
            >
                <i class="fa-fw fa fa-check"></i>
            </ButtonJaffa>
            <i class="fa fa-fw fa-times text-danger"></i>
        </div>
      </div>
      <div class="d-flex flex-row justify-content-between align-items-center rows-striped">
        <div>Moteurs niryo</div>
        <div v-if="!niryoMotorsErrorMode">
          <i class="fa fa-fw fa-check text-jaffa"></i>
        </div>
        <div v-else>
            <ButtonJaffa
                size="sm"
                @click="ackNiryoMotorsError"
            >
                <i class="fa-fw fa fa-check"></i>
            </ButtonJaffa>
            <i class="fa fa-fw fa-times text-danger"></i>
        </div>
      </div>
    </div>
    <!--<div class="border-deepdark rounded p-3 d-flex flex-column mb-2">
      <div class="mb-1">États de l'imprimante</div>
      <div class="d-flex flex-row">
        <div v-for="state in printerStates" :key="state.name" class="align-items-center d-flex mr-not-last">
          <div
            class="d-flex justify-content-center align-items-center mr-2"
            style="border: 1px var(--light) solid; border-radius: 50%; width: 31px; height: 31px"
          >
            <i :class="state.icon"></i>
          </div>
          <ButtonJaffa><i :class="state.actionIcon"></i></ButtonJaffa>
        </div>
      </div>
    </div>-->

    <div v-if="isInMaintenanceMode">
      <div v-for="motor in niryoMotors" :key="motor.id" class="d-flex flex-column mb-2">
        <div class="d-flex justify-content-between align-items-center mb-1">
            <div class="text-one-line-ellipsis min-width-100px">{{ motor.name }}</div>

            <b-button-group>
            <ButtonJaffa
                class="position-relative"
                size="sm"
                :disabled="parseInt(motor.stepDelay) > parseInt(motor.liminaryStepDelay) && parseInt(motor.nLiminarySteps) > 0"
                @click="() => motorMove(motor.channel, 'motor_forward', motor.id, parseInt(motor.nSteps), parseInt(motor.stepDelay), parseInt(motor.nLiminarySteps), parseInt(motor.liminaryStepDelay))"
            >
                <i class="fa-fw fas fa-angle-double-left"></i>
                <i
                  v-if="motor.forwardHasLimitSwitch != null"
                  class="fa-fw fas fa-home position-absolute"
                  style="scale: 0.7; bottom: 0; right: 0"
                  :style="{color: motor.forwardHasLimitSwitch ? '#cb4299' : 'inherit'}"
                ></i>
            </ButtonJaffa>
            <ButtonJaffa
                class="position-relative"
                size="sm"
                :disabled="parseInt(motor.stepDelay) > parseInt(motor.liminaryStepDelay) && parseInt(motor.nLiminarySteps) > 0"
                @click="() => motorMove(motor.channel, 'motor_backward', motor.id, parseInt(motor.nSteps), parseInt(motor.stepDelay), parseInt(motor.nLiminarySteps), parseInt(motor.liminaryStepDelay))"
            >
                <i class="fa-fw fas fa-angle-double-right"></i>
                <i
                  v-if="motor.backwardHasLimitSwitch != null"
                  class="fa-fw fas fa-home position-absolute"
                  style="scale: 0.7; bottom: 0; right: 0"
                  :style="{color: motor.backwardHasLimitSwitch ? '#cb4299' : 'inherit'}"
                ></i>
            </ButtonJaffa>
            <ButtonJaffa
                size="sm"
                @click="() => motorStop(motor.channel, motor.id)"
            >
                <i class="fa-fw fas fa-pause"></i>
            </ButtonJaffa>
            </b-button-group>
        </div>
        <!--<div class="d-flex mb-1">
          <b-input class="w-25" v-model="motor.nSteps" placeholder="Steps" type="number" min="0" max="20000"></b-input>
          <b-input class="w-25" v-model="motor.stepDelay" placeholder="Délais inter-step (µs)" type="number" min="200" max="20000"></b-input>
          <b-input class="w-25" v-model="motor.nLiminarySteps" placeholder="Steps liminaires" type="number" min="0" max="20000"></b-input>
          <b-input class="w-25" v-model="motor.liminaryStepDelay" placeholder="Délais initial (µs)" type="number" min="200" max="20000"></b-input>
        </div>-->
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
  </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"
import preferenceStore from '@/store/preferenceStore.js'

export default {
  name: "WidgetWaffleFactory",
  components: {
    ButtonJaffa,
  },
  data() {
    return {
      currentStateIndex: 0,
      printerStates: [
        {
          name: "Far from home",
          icon: "fas fa-fw fa-exclamation-triangle",
          actionIcon: "fas fa-fw fa-home",
        },
        {
          name: "Hey",
          icon: "fas fa-fw fa-home",
          actionIcon: "fas fa-fw fa-tint",
        },
        {
          name: "Hey",
          icon: "fas fa-fw fa-tint",
          actionIcon: "fas fa-fw fa-play",
        },
      ],
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
    hasHomingBeenRun() {
      return roomStore.state.sessionData[this.roomId].waffle_factory_printer_has_homing_been_run
    },
    printerCurrentAction() {
      return roomStore.state.sessionData[this.roomId].waffle_factory_printer_current_action
    },
    motorsErrorMode() {
      return roomStore.state.sessionData[this.roomId].waffle_factory_motors_error_mode
    },
    limitSwitches() {
      return roomStore.state.sessionData[this.roomId].waffle_factory_motors_limit_switches
    },
    niryoLimitSwitches() {
      return roomStore.state.sessionData[this.roomId].niryo_motors_limit_switches
    },
    niryoMotorsErrorMode() {
      return roomStore.state.sessionData[this.roomId].niryo_motors_error_mode
    },
    isInMaintenanceMode() {
      return preferenceStore.state.isInMaintenanceMode
    },
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
          forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['niryo'] : null,
          backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['niryo'] : null,
        },
        {
          name: "Convoyeur Imprimante",
          id: "printer",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['printer'] : null,
          backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['printer'] : null,
        },
        {
          name: "Tirette extraction",
          id: "extractor",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['extractor'] : null,
          backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['extractor'] : null,
        },
        {
          name: "Tirette recharge",
          id: "reloader",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['reloader'] : null,
          backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['reloader'] : null,
        },
        {
          name: "Convoyeur court",
          id: "short_one",
          channel: 'waffle_factory',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['short_one'] : null,
          backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['short_one'] : null,
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
            forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['podium'] : null,
            backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['podium'] : null,
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
          forwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.forward['finisher'] : null,
          backwardHasLimitSwitch: this.limitSwitches ? this.limitSwitches.backward['finisher'] : null,
        },
        {
          name: "Niryo moteur épaule",
          id: "shoulder",
          channel: 'niryo',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.niryoLimitSwitches ? this.niryoLimitSwitches.forward['shoulder'] : null,
          backwardHasLimitSwitch: this.niryoLimitSwitches ? this.niryoLimitSwitches.backward['shoulder'] : null,
        },
        {
          name: "Niryo moteur bras",
          id: "arm",
          channel: 'niryo',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.niryoLimitSwitches ? this.niryoLimitSwitches.forward['arm'] : null,
          backwardHasLimitSwitch: this.niryoLimitSwitches ? this.niryoLimitSwitches.backward['arm'] : null,
        },
        {
          name: "Niryo moteur coude",
          id: "elbow",
          channel: 'niryo',
          nSteps: 100,
          stepDelay: 2000,
          nLiminarySteps: 0,
          liminaryStepDelay: 3000,
          forwardHasLimitSwitch: this.niryoLimitSwitches ? this.niryoLimitSwitches.forward['elbow'] : null,
          backwardHasLimitSwitch: this.niryoLimitSwitches ? this.niryoLimitSwitches.backward['elbow'] : null,
        },
      ]

      return motors
    }
  },
  methods: {
    runHomingAndPurge() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          action: 'run_homing_and_purge',
        }
      )
    },
    ackNiryoMotorsError() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          action: 'ack_niryo_motors_error',
        }
      )
    },
    ackMotorsError() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'waffle_factory',
          widgetType: 'waffle_factory',
          action: 'ack_motors_error',
        }
      )
    },
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
    "roomId",
  ]
}
</script>

<style scoped>
.max-width-100px {
  max-width: 100px;
}

.mr-not-last:not(:last-child) {
  margin-right: 0.5rem;
}
</style>