<template>
  <div class="container h-100">
    <div class="row h-100">
      <div class="col-6 d-flex align-items-center">
        <img src="@/assets/pizzage.png" class="img-fluid">
      </div>
      <div class="col-6 d-flex flex-column justify-content-between py-3">
        <div>
          <h5>{{ $t(itemId) }}</h5>
          <p class="mb-0">{{ $t(itemId + '_desc') }}</p>
        </div>
        <div class="text-right">
          <b-btn-group>
            <b-btn @click="minusOne" class="lh-1" variant="outline-primary"><i class="fa fa-minus"></i></b-btn>
            <UnclickableButton>{{ quantity }}</UnclickableButton>
            <b-btn @click="plusOne" class="lh-1" variant="outline-primary"><i class="fa fa-plus"></i></b-btn>
          </b-btn-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UnclickableButton from '@/components/UnclickableButton.vue'
import orderStore from '@/store/orderStore.js'

export default {
  name: "OrderableItem",
  components: {
    UnclickableButton,
  },
  computed: {
    quantity: function() {
      return orderStore.state.items[this.itemId].quantity
    }
  },
  methods: {
    minusOne: function() {
      orderStore.commit('minusOne', this.itemId)
    },
    plusOne: function() {
      orderStore.commit('plusOne', this.itemId)
    },
  },
  props: ["itemId"],
}
</script>
