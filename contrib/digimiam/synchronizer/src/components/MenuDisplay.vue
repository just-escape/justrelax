<template>
  <div class="position-relative h-100">
    <div class="d-flex flex-column h-100">
      <div class="menu-container px-2 pb-1 position-relative mb-4 h-100">
        <div class="menu-frame"></div>
        <div class="menu-background"></div>
        <div class="menu-title-ribbon mb-2 text-right p-2">
          <img src="@/assets/img/pyramid.svg" class="mb-1" height="18px"/> {{ $t('digimiam_menu') }}
        </div>
        <div class="date text-right mb-5 mt-2">
          {{ date }}
        </div>

        <div class="position-relative">
          <MenuItemCursor class="position-absolute"/>
          <MenuItem
            v-for="(item, itemIndex) in menuItems"
            class="pl-4"
            :key="item.id"
            :itemIndex="itemIndex"
          />
        </div>

        <MenuLoadingWidget :startAnimationSignal="startAnimationSignal"/>
      </div>

      <div class="position-relative" :style="{opacity: autoValidateDishes ? 0 : 1}" style="transition: opacity 4s ease-in-out">
        <div class="glowing-wire left-wire"></div>
        <div class="glowing-wire right-wire"></div>
        <ButtonValidate @click="validate" class="btn-block" :disabled="success || autoValidateDishes"/>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonValidate from '@/components/ButtonValidate.vue'
import MenuItemCursor from '@/components/MenuItemCursor.vue'
import MenuLoadingWidget from '@/components/MenuLoadingWidget.vue'
import MenuItem from '@/components/MenuItem.vue'
import menuStore from '@/store/menuStore.js'

export default {
  name: 'MenuDisplay',
  components: {
    ButtonValidate,
    MenuItemCursor,
    MenuLoadingWidget,
    MenuItem,
  },
  data() {
    return {
      date: undefined,
      startAnimationSignal: false,
    }
  },
  computed: {
    autoValidateDishes: function() {
      return menuStore.state.autoValidateDishes
    },
    dragging: function() {
      return menuStore.state.dragging
    },
    lang: function() {
      return this.$i18n.locale
    },
    menuItems: function() {
      return menuStore.state.menuItems
    },
    success: function() {
      return menuStore.state.success
    },
  },
  methods: {
    refreshDate: function() {
      var date = new Date()
      date.setFullYear(2080)
      this.$moment.locale(this.lang)
      this.date = this.$moment(date).format('LL')
    },
    validate: function() {
      if (menuStore.state.success || menuStore.state.validating) {
        return
      }

      this.startAnimationSignal = !this.startAnimationSignal

      menuStore.commit("lockValidate")
      setTimeout(this.validatePostAnimation, 1550)
    },
    validatePostAnimation: function() {
      menuStore.commit("unlockValidate")
      menuStore.commit("validateMenu", menuStore.getters)
    },
  },
  watch: {
    lang: function() {
      this.refreshDate()
    }
  },
  mounted() {
    this.refreshDate()
  }
}
</script>

<style scoped>
.menu-container {
  border: 1px solid transparent;
  border-top: 9px solid transparent;
  padding-top: 38px;
}

.menu-background {
  background-color: rgba(00, 45, 64, 0.5);
  position: absolute;
  top: -9px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 6px),
    calc(43px + 6px) 0px
  );
  z-index: -1;
}

.menu-frame {
  position: absolute;
  left: -1px;
  top: -9px;
  right: -1px;
  bottom: -1px;
  filter: drop-shadow(1px 1px 4px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(100% - 1px) -10px,
    calc(100% + 10px) -10px,
    calc(100% + 10px) calc(100% + 10px),
    -10px calc(100% + 6px),
    -10px calc(48px - 7px - 6px),
    calc(48px + 2px - 6px) -10px,
    calc(100% - 1px) -10px,
    calc(100% - 1px) 9px,
    calc(48px + 1px) 9px,
    1px 48px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 1;
}

.menu-frame::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    calc(100% - 1px) 0%,
    100% 0%,
    100% 100%,
    0% 100%,
    0% calc(48px - 7px),
    calc(48px + 2px) 0%,
    calc(100% - 1px) 0%,
    calc(100% - 1px) 9px,
    calc(48px + 1px) 9px,
    1px 48px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 10;
}

.menu-title-ribbon {
  position: absolute;
  width: 100%;
  height: 40px;
  top: 0;
  right: 0;
  border-bottom: 1px solid #00d1b6;
  background-color: rgba(00, 45, 64, 0.6);
  font-size: 20px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 9px),
    43px 0px
  );
}

.date {
  font-size: 14px;
  z-index: 11;
}

.glowing-wire {
  position: absolute;
  height: 24px;
  width: 1px;
  bottom: 40px;
  border-left: 1px solid #00d1b6;
  box-shadow: 1px 0px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.left-wire {
  left: 20%;
}

.right-wire {
  right: 20%;
}
</style>
