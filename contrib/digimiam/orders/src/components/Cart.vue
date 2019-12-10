<template>
  <div class="container h-100 overflow-hidden position-relative">
    <button @click="add">Add</button>
    <button @click="removeAll">Remove all</button>
    <transition-group
      name="list-complete"
      tag="div"
      class="row"
    >
      <div
        v-for="item in items"
        :key="item.id"
        class="col-3 list-complete-item p-0"
        :class="{deleting: item.deleting}"
      >
        <img src="@/assets/pizzage.png" class="m-1 img-fluid">
      </div>
    </transition-group>
    <div class="position-absolute" style="margin-left: -15px; bottom: 0; height: 100px; width: 70%; background: black; color: white">
      poubelle
    </div>
  </div>
</template>

<script>
export default {
  name: "Cart",
  data() {
    return {
      items: [
        {
          id: 1,
          deleting: false,
        },
        {
          id: 2,
          deleting: false,
        },
        {
          id: 3,
          deleting: false,
        },
      ],
      maxItems: 12,
      nextNum: 10,
    }
  },
  methods: {
    randomIndex: function() {
      return Math.floor(Math.random() * this.items.length)
    },
    add: function() {
      if (this.items.length < this.maxItems) {
        this.items.splice(0, 0, {id: this.nextNum++, deleting: false})
      }
    },
    removeAll: function() {
      this.items = []
      /*for (var i = 0 ; i < this.items.length ; i++) {
        this.items[i].deleting = true
      }

      this.$anime({
        targets: '.deleting',
        translateX: 500,
        duration: 2000,
        easing: 'linear',
      })*/
    },
  }
}
</script>

<style scoped>
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
</style>
