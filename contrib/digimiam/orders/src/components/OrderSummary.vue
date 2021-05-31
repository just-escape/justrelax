<template>
  <div class="position-relative d-flex flex-column flex-grow-1">
    <CreditsNotification class="position-absolute" :displayed="displayCreditsNotification" @ok="acknowledgeCreditsNotification" :class="{'shaking-more': creditsNotificationShaking}"/>
    <ResumeOrderNotification class="position-absolute" :displayed="displayResumeOrderNotification" @ok="acknowledgeResumeNotification"/>
    <OrderRecapNotification class="position-absolute" :displayed="displayOrderRecapNotification" @ok="acknowledgeRecapNotification"/>

    <div class="overflow-hidden p-4">
      <div class="d-flex flex-row justify-content-start align-items-end ml-3 mb-3 px-2 position-relative">
        <div class="w-50 mr-3">
          <OrderConfirmButton
            :pulse="cartItems.length && !isOrderOnHold"
            :gray="isRestaurantClosed"
            :disabled="!cartItems.length || isOrderOnHold"
            @click="confirm"
          >
            {{ $t('confirm_order') }}
          </OrderConfirmButton>
        </div>

        <div class="btn-group h-100" role="group" :class="{shaking: creditsShaking}" :style="{opacity: !cartItems.length || isRestaurantClosed ? 0.4 : 1}">
          <b-btn :variant="getCreditsVariant" class="text-left py-2" style="width: 110px" disabled>
            {{ "Crédits" }}
          </b-btn>
          <b-btn :variant="getCreditsVariant" class="py-2 pr-0" style="width: 50px" disabled>
            {{ credits }}
          </b-btn>
          <b-btn :variant="getCreditsVariant" class="py-2" disabled>
            {{ $t('nF') }}
          </b-btn>
        </div>
      </div>

      <div class="d-flex flex-row justify-content-start align-items-center ml-3 px-2">
        <div class="w-50 mr-3">
          <b-btn
            block
            :variant="isRestaurantClosed ? 'outline-secondary' : 'outline-info'"
            class="py-2"
            :disabled="!cartItems.length || isOrderOnHold"
            :style="{opacity: !cartItems.length || isOrderOnHold ? 0.4 : 1}"
            @click="reset"
          >
            {{ $t('reset_order') }}
          </b-btn>
        </div>

        <div class="btn-group" role="group" :style="{opacity: !cartItems.length || isRestaurantClosed ? 0.4 : 1}">
          <b-btn :variant="isRestaurantClosed ? 'outline-secondary' : 'outline-info'" class="py-2" style="width: 110px" disabled>
            {{ $t('total_price') }}
          </b-btn>
          <b-btn :variant="isRestaurantClosed ? 'outline-secondary' : 'outline-info'" class="py-2 pr-0" style="width: 50px" disabled>
            {{ totalPrice }}
          </b-btn>
          <b-btn :variant="isRestaurantClosed ? 'outline-secondary' : 'outline-info'" class="py-2" disabled>
            {{ $t('nF') }}
          </b-btn>
        </div>
      </div>

      <div class="container position-relative" style="min-height: 113px">
        <transition-group
          tag="div"
          name="list-complete"
          class="row"
        >
          <OrderSummaryItem
            v-for="item in cartItems"
            :key="item.increment"
            :itemId="item.itemId"
            :variation="item.variation"
            class="col-3 list-complete-item p-0"
          />
        </transition-group>

        <div class="position-absolute w-100 h-100 d-flex justify-content-center align-items-center" style="top: 0; left: 0">
          <div class="text-light text-center px-3 py-1 blinking rounded" :class="{'d-none': !isCartFull}" style="background-color: orangered">
            <div class="font-weight-bold"> {{ $t('cart_full') }}</div>
            <div class="small">{{ $t('confirm_or_reset_order') }}</div>
          </div>
        </div>

        <div class="position-absolute w-100 h-100 d-flex justify-content-center align-items-center" style="top: 0; left: 0">
          <div class="text-light text-center px-3 py-1 blinking rounded" :class="{'d-none': !displayEmptyCartHelp}" style="background-color: var(--info)">
            <div class="font-weight-bold"> {{ $t('empty_cart') }}</div>
            <div class="small">{{ $t('add_an_item') }}</div>
          </div>
        </div>
      </div>
    </div>

    <WarningClosed v-if="isRestaurantClosed"/>
  </div>
</template>

<script>
import OrderSummaryItem from '@/components/OrderSummaryItem.vue'
import OrderConfirmButton from '@/components/OrderConfirmButton.vue'
import WarningClosed from '@/components/WarningClosed.vue'
import ResumeOrderNotification from '@/components/ResumeOrderNotification.vue'
import OrderRecapNotification from '@/components/OrderRecapNotification.vue'
import CreditsNotification from '@/components/CreditsNotification.vue'
import orderStore from '@/store/orderStore.js'
import progressionStore from '@/store/progressionStore.js'
import publishSubscribreService from '@/store/publishSubscribeService.js'

export default {
  name: "OrderSummary",
  components: {
    OrderSummaryItem,
    OrderConfirmButton,
    WarningClosed,
    ResumeOrderNotification,
    OrderRecapNotification,
    CreditsNotification,
  },
  data() {
    return {
      creditsNotificationCounter: 0,
      displayCreditsNotification: false,
      creditsNotificationShaking: false,
      creditsNotificationShakingTask: null,
      creditsShaking: false,
      creditsShakingTask: null,
      autocloseNotification: null,
    }
  },
  computed: {
    getCreditsVariant: function () {
      if (this.isRestaurantClosed) {
        return 'outline-secondary'
      } else if (this.credits < this.totalPrice) {
        return 'outline-danger'
      } else if (this.totalPrice === 0) {
        return 'outline-light'
      } else {
        return 'outline-success'
      }
    },
    isCartFull: function() {
      return orderStore.getters.isCartFull
    },
    cartItems: function() {
      return orderStore.state.cartItems
    },
    credits: function() {
      return orderStore.state.credits
    },
    totalPrice: function() {
      return orderStore.getters.totalPrice
    },
    isOrderOnHold: function() {
      return progressionStore.state.isOrderOnHold
    },
    isRestaurantClosed: function() {
      return progressionStore.state.isRestaurantClosed
    },
    displayResumeOrderNotification: function() {
      return orderStore.state.displayResumeOrderNotification
    },
    displayOrderRecapNotification: function() {
      return orderStore.state.displayOrderRecapNotification
    },
    displayEmptyCartHelp: function() {
      return orderStore.state.displayEmptyCartHelp && this.cartItems.length === 0
    },
  },
  methods: {
    acknowledgeCreditsNotification: function() {
      this.displayCreditsNotification = false
    },
    reset: function() {
      orderStore.commit('resetOrder')
    },
    stopCreditsShaking: function() {
      this.creditsShaking = false
    },
    stopCreditsNotificationShaking: function() {
      this.creditsNotificationShaking = false
    },
    confirm: function() {
      if (this.credits >= this.totalPrice) {
        orderStore.commit('confirmOrder')
        progressionStore.commit('setIsOrderOnHold', true)
      } else {
        if (this.displayCreditsNotification === false) {
          this.creditsNotificationCounter++
          if (this.creditsNotificationCounter % 3 == 0) {
            this.displayCreditsNotification = true
          }
        } else {
          this.creditsNotificationShaking = true
          clearTimeout(this.creditsShaking)
          this.creditsNotificationShakingTask = setTimeout(this.stopCreditsNotificationShaking, 400)
        }

        this.creditsShaking = true
        clearTimeout(this.creditsShaking)
        this.creditsShakingTask = setTimeout(this.stopCreditsShaking, 400)
      }
    },
    acknowledgeResumeNotification() {
      orderStore.commit('setDisplayResumeOrderNotification', false)
      publishSubscribreService.commit('publish', {'category': 'resume_order'})
    },
    acknowledgeRecapNotification() {
      console.log('ack recap')
    },
  },
  watch: {
    credits(newValue) {
      if (newValue >= this.totalPrice) {
        this.displayCreditsNotification = false
      }
    }
  }
}
</script>

<style scoped>
.list-complete {
  transition: all 1s;
}

.list-complete-item {
  transition: all 1s;
}

.list-complete-enter {
  transform: translateX(-100%);
}

.list-complete-leave-to {
  opacity: 0;
  transform: translateY(500px);
}

.list-complete-leave-active {
  position: absolute;
}

.very-small {
  font-size: 0.7rem;
}

.btn-outline-danger {
  border-color: orangered;
  color: orangered;
}

.btn:disabled {
  opacity: 1;
}

.shaking {
  animation: shaker 0.8s 1 linear;
}

@keyframes shaker {
  0% { transform: translate(20px); }
  20% { transform: translate(-20px); }
  40% { transform: translate(10px); }
  60% { transform: translate(-10px); }
  80% { transform: translate(6px); }
  100% { transform: translate(0px); }
}

.shaking-more {
  animation: shaker-more 0.8s 1 linear;
}

@keyframes shaker-more {
  0% { transform: translate(30px); }
  15% { transform: translate(-30px); }
  45% { transform: translate(15px); }
  55% { transform: translate(-15px); }
  85% { transform: translate(8px); }
  100% { transform: translate(0px); }
}
</style>
