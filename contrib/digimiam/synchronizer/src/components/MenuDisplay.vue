<template>
  <div class="position-relative h-100">
    <div class="d-flex flex-column h-100">
      <div class="menu-container px-2 pb-1 position-relative mb-3 h-100">
        <div class="menu-frame"></div>
        <div class="menu-background"></div>
        <div class="menu-title-ribbon mb-2 text-right p-2">
          {{ $t('digimiam_menu') }}
        </div>
        <div class="date text-right mb-5">
            {{ date }}
        </div>

        <MenuItem
          v-for="(item, itemIndex) in menuItems"
          :key="item.id"
          :itemIndex="itemIndex"
        />
      </div>

      <div class="position-relative">
        <div class="glowing-wire left-wire"></div>
        <div class="glowing-wire right-wire"></div>
        <ButtonActivate class="btn-block"/>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonActivate from '@/components/ButtonActivate.vue'
import MenuItem from '@/components/MenuItem.vue'
import menuStore from '@/store/menuStore.js'
import l10nStore from '@/store/l10nStore.js'

export default {
  name: 'MenuDisplay',
  components: {
    ButtonActivate,
    MenuItem,
  },
  data() {
    return {
      date: undefined
    }
  },
  computed: {
    lang: function() {
      return l10nStore.state.lang
    },
    menuItems: function() {
      return menuStore.state.menuItems
    }
  },
  methods: {
    refreshDate: function() {
      var date = new Date()
      date.setFullYear(2080)
      this.$moment.locale(this.lang)
      this.date = this.$moment(date).format('LL')
    }
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
    43px 0px
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
    -10px calc(43px - 7px - 6px),
    calc(43px + 2px - 6px) -10px,
    calc(100% - 1px) -10px,
    calc(100% - 1px) 9px,
    calc(43px + 1px) 9px,
    1px 43px,
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
    0% calc(43px - 7px),
    calc(43px + 2px) 0%,
    calc(100% - 1px) 0%,
    calc(100% - 1px) 9px,
    calc(43px + 1px) 9px,
    1px 43px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 10;
}

.menu-title-ribbon {
  position: absolute;
  width: 100%;
  height: 34px;
  top: 0;
  right: 0;
  border-bottom: 1px solid #00d1b6;
  background-color: rgba(00, 45, 64, 0.6);
  font-size: 18px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 9px),
    43px 0px
  );
}

.date {
  font-size: 10px;
  z-index: 11;
}

.glowing-wire {
  position: absolute;
  height: 16px;
  width: 1px;
  bottom: 36px;
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
