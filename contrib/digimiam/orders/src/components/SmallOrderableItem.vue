<template>
  <div class="container h-100">
    <div class="row h-100">
      <div class="col-2 d-flex align-items-center px-0">
        <img src="@/assets/pizzage.png" class="img-fluid">
      </div>
      <div class="col-10 d-flex flex-row justify-content-between align-items-center pr-0">
        <div>
          <h5 class="font-weight-bold mb-0">{{ $t(itemId) }}</h5>
        </div>
        <div>
          <b-btn-group>
            <b-btn @click="minusOne" class="lh-1" variant="outline-primary" size="sm">
              <i class="small-font fa fa-minus"></i>
            </b-btn>
            <UnclickableOutlinePrimaryButton class="small-font align-items-center" size="sm">
              {{ quantity }}
            </UnclickableOutlinePrimaryButton>
            <b-btn @click="plusOne" class="lh-1" variant="outline-primary" size="sm">
              <i class="small-font fa fa-plus"></i>
            </b-btn>
          </b-btn-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UnclickableOutlinePrimaryButton from '@/components/UnclickableOutlinePrimaryButton.vue'
import orderStore from '@/store/orderStore.js'

export default {
  name: "SmallOrderableItem",
  components: {
    UnclickableOutlinePrimaryButton,
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
  props: {
    "itemId": {
      type: String,
    },
  }
}
</script>

<style scoped>
.small-font {
  font-size: 70%;
}
</style>