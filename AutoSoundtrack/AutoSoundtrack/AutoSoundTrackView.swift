//
//  AutoSoundTrackView.swift
//  AutoSoundtrack
//
//  Created by Matthews Ma on 2023-09-16.
//

import SwiftUI



struct AutoSoundTrackView: View {
    @ObservedObject var viewModel = AutoSoundtrackViewModel()
    var body: some View {
        CameraView()
    }
}

struct AutoSoundTrackView_Previews: PreviewProvider {
    static var previews: some View {
        AutoSoundTrackView()
    }
}
